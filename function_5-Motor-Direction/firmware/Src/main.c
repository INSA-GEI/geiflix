
/**
 ******************************************************************************
 * @file           : main.c
 * @brief          : Main program body
 ******************************************************************************
 ** This notice applies to any and all portions of this file
 * that are not between comment pairs USER CODE BEGIN and
 * USER CODE END. Other  portions of this file, whether
 * inserted by the user or by software development tools
 * are owned by their respective copyright owners.
 *
 * COPYRIGHT(c) 2018 STMicroelectronics
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *   1. Redistributions of source code must retain the above copyright notice,
 *      this list of conditions and the following disclaimer.
 *   2. Redistributions in binary form must reproduce the above copyright notice,
 *      this list of conditions and the following disclaimer in the documentation
 *      and/or other materials provided with the distribution.
 *   3. Neither the name of STMicroelectronics nor the names of its contributors
 *      may be used to endorse or promote products derived from this software
 *      without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 ******************************************************************************
 */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "stm32f1xx_hal.h"
#include "adc.h"
#include "can.h"
#include "dma.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"
#include "power.h"
#include "control.h"
#include "calibrate.h"
#include "GPS.h"


/* USER CODE BEGIN Includes */

/* Modes definition
 * 0- Calibration
 * 1- Motor command by CAN frame 0x010 (CMC)
 * 2- Motor command by CAN frame 0x020 (SSC)
 * 3- Autonomous movement to one destination without GPS connection
 * 4- Autonomous movement to several destination without GPS connection + routine fire detection at each location
 * 5- Autonomous movement to several destination with GPS connection + routine fire detection at each location
 */

#define MODE 5
#define JOG_SPEED 0.17 	// speed in meter/s when speed set at JOG
#define nbDestCoordinates 2 // number of coordinates in the path
#define nbCarCoordinates 50 // number of coordinates of the car received to calculate car position

/* USER CODE END Includes */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */
/* Private variables ---------------------------------------------------------*/
int UPDATE_CMD_FLAG = 1;
int SEND_CAN = 1;

/* Tous ADC sur 12 bits pleine echelle 3.3V
 ADCBUF[0] mesure batterie
 ADCBUF[1] angle volant
 ADCBUF[2] I moteur arriere gauche
 ADCBUF[3] I moteur arriere droit
 ADCBUF[4] I moteur avant
 */
uint32_t ADCBUF[5];

int cmdLRM = 50, cmdRRM = 50, cmdSFM = 50, cmdPOS = 50; // 0 � 100 Moteur gauche, droit, avant, angle avant

uint32_t VMG_mes = 0, VMD_mes = 0, per_vitesseG = 0, per_vitesseD = 0;

/* Enable Moteurs 				*/
/* GPIO_PIN_SET : activation    */
/* GPIO_PIN_RESET : pont ouvert */
GPIO_PinState en_MARG = GPIO_PIN_RESET;
GPIO_PinState en_MARD = GPIO_PIN_RESET;
GPIO_PinState en_MAV = GPIO_PIN_RESET;
GPIO_PinState en_POS = GPIO_PIN_RESET;

/********************************Informations rotation volant********************************/
/* mesure angulaire potentiometre amplitudes volant +/- 17 % environ autour du centre        */
/* PWM = 0.5 (50) % arret, PWM = 0.4 tourne gauche, PWM = 0.6 tourne droite                  */ 

CanTxMsgTypeDef TxMessage;
CanRxMsgTypeDef RxMessage;
uint8_t data[8] = {0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88};

int modeSpeed = 0;
int modeSteer = 0;

// data of GPS coordinates received in the CAN frame
double latDegPos = 0;
double latMinPos = 0;
double latSecPos = 0;
double latTenPos = 0;
double lonDegPos = 0;
double lonMinPos = 0;
double lonSecPos = 0;
double lonTenPos = 0;


double latDegDes = 0;
double latMinDes = 0;
double latSecDes = 0;
double latTenDes = 0;
double lonDegDes = 0;
double lonMinDes = 0;
double lonSecDes = 0;
double lonTenDes = 0;

// GPS coordinates of the car
double carLatitude = 0;
double carLongitude = 0;
double angleCar = 0;

double carLatitudeStart ;
double carLongitudeStart ;

double carCoordinates[2];
double listCarCoordinates[nbCarCoordinates][2];
int indexCarCoordinates = 0;
double meanCarLatitude = 0;
double meanCarLongitude = 0;

// GPS coordinates of destinations
double destLatitude = 0;
double destLongitude = 0;


double destCoordinates[2];
double listDestCoordinates[nbDestCoordinates][2];
int indexDestCoordinates = 0;

// destination achieved : 1 if the car is arrived at the destination
int pos_OK = 0;

// fire detection : 1 if a fire is detected, 0 otherwise
int isFire = 0;

double dist =0;

extern CAN_HandleTypeDef hcan;

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);

/* USER CODE BEGIN PFP */
/* Private function prototypes -----------------------------------------------*/

/* USER CODE END PFP */

/* USER CODE BEGIN 0 */
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim){
    if (htim->Instance==TIM2)
    {
        VMG_mes = 0;
    } else if (htim->Instance==TIM4){
        VMD_mes = 0;
    }
}

void HAL_TIM_IC_CaptureCallback(TIM_HandleTypeDef *htim)
{
    /***               Mesures des vitesses moteurs                      ***
     * F�quences entr�es micro, sorties capteurs, entre environ 2hz � 80 hz *
     * Timer 2,4 sur 16 bits (65535)cp ->compte p�riode 9999 pour 1s (1Hz)   *
     *                               ->compte p�riode 1000 pour 0.1s (10Hz)  *
     * Rapport r�duction 2279/64 ~ 36 impulsions/tour de roue                *
     * unite de 0.01*tr/mn = 168495/ cp                                     *
     */
    if (htim->Instance==TIM2)
    {
        per_vitesseG =	HAL_TIM_ReadCapturedValue (&htim2,TIM_CHANNEL_3);//PB10
        VMG_mes = 1684949/per_vitesseG ;// X 0.01 tr/mn
        
        __HAL_TIM_SET_COUNTER(&htim2,0);// mise a zero compteur apres capture
    }
    if (htim->Instance==TIM4)
    {
        per_vitesseD =	HAL_TIM_ReadCapturedValue (&htim4,TIM_CHANNEL_3);//PB8
        VMD_mes = 1684949/per_vitesseD ;// X 0.01 tr/mn
        
        __HAL_TIM_SET_COUNTER(&htim4,0);// mise a zero compteur apres capture
    }
}

/* USER CODE END 0 */

/**
 * @brief  The application entry point.
 *
 * @retval None
 */
int main(void)
{
    /* USER CODE BEGIN 1 */
    hcan.pTxMsg = &TxMessage;
    hcan.pRxMsg = &RxMessage;
    /* USER CODE END 1 */
    
    /* MCU Configuration----------------------------------------------------------*/
    
    /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
    HAL_Init();
    
    /* USER CODE BEGIN Init */
    
    /* USER CODE END Init */
    
    /* Configure the system clock */
    SystemClock_Config();
    
    /* USER CODE BEGIN SysInit */
    
    /* USER CODE END SysInit */
    
    /* Initialize all configured peripherals */
    MX_GPIO_Init();
    power_boostrap();
    
    MX_DMA_Init();
    MX_USART2_UART_Init();
    MX_TIM1_Init();
    MX_TIM2_Init();
    MX_TIM4_Init();
    MX_ADC1_Init();
    MX_CAN_Init();
    /* USER CODE BEGIN 2 */
    
    /* Initialisations */
    
    /* PWM MOTEURS */
    HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);
    HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_2);
    HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_3);
    
    //Sorties complementaires
    HAL_TIMEx_OCN_Start(&htim1,TIM_CHANNEL_1);
    HAL_TIMEx_OCN_Start(&htim1,TIM_CHANNEL_2);
    HAL_TIMEx_OCN_Start(&htim1,TIM_CHANNEL_3);
    /*Vitesse*/
    __HAL_TIM_ENABLE_IT(&htim2, TIM_IT_UPDATE);
    __HAL_TIM_ENABLE_IT(&htim4, TIM_IT_UPDATE);
    HAL_TIM_IC_Start_IT (&htim2,TIM_CHANNEL_3);//autorisation IT capture CH3
    HAL_TIM_IC_Start_IT (&htim4,TIM_CHANNEL_3);//autorisation IT capture CH3
    
    /* ADC1 */
    HAL_ADC_Start_DMA (&hadc1,ADCBUF,5);
    
    /* USER CODE END 2 */
    
    /* Infinite loop */
    /* USER CODE BEGIN WHILE */
    
    /* Initialisation Steering */
    //steering_Init();


    while (1)
    {
        /* USER CODE END WHILE */
        /* USER CODE BEGIN 3 */

        /* Update motors command*/
        if (UPDATE_CMD_FLAG){
            UPDATE_CMD_FLAG = 0;

            /* calibration */
			#if (MODE == 0)
            	calibrate();

           /* Motor command by CAN frame 0x010 (CMC) */
			#elif (MODE == 1)
            	wheels_set_speed(en_MARD, en_MARG, cmdRRM, cmdLRM);
                en_POS = GPIO_PIN_SET;
                // Assure la non-contradiction des commandes moteurs
                if ((en_MAV == GPIO_PIN_SET) && (en_POS == GPIO_PIN_SET)) {
                	en_MAV = GPIO_PIN_RESET;
                }
                if (!steering_is_a_button_pressed()) {
                    //steering_set_speed(en_MAV, cmdSFM);
                    steering_set_position(en_POS, cmdPOS);
                }
                steering_move_with_button();

            /* Motor command by CAN frame 0x020 (SSC) */
			#elif (MODE == 2)
                modeSpeed = 50;
                modeSteer = 50;
                car_control(modeSpeed, modeSteer);

            /* autonomous movement to one destination without GPS connection */
			#elif (MODE == 3)
    			carLatitude = 43.570630;
    			carLongitude = 1.466440;
            	carLatitudeStart = carLatitude;
            	carLongitudeStart = carLongitude;

            	destLatitude = 43.570670;
            	destLongitude = 1.466460;

            	movement_without_GPS(carLatitudeStart, carLongitudeStart, destLatitude, destLongitude);


            /* autonomous movement to several destination without GPS connection + routine fire detection at each location */
			#elif (MODE == 4)

            /* receive coordinates of the path and store it*/
            if (latDegDes != 0) {
            	if (indexDestCoordinates <= nbDestCoordinates) {
                	listDestCoordinates[indexDestCoordinates][0] = dms2dd(latDegDes, latMinDes, latSecDes, latTenDes);
                	listDestCoordinates[indexDestCoordinates][1] = dms2dd(lonDegDes, lonMinDes, lonSecDes, lonTenDes);
                	dest_coordinates_to_zero();
                	destLatitude = listDestCoordinates[indexDestCoordinates][0];
                	destLongitude = listDestCoordinates[indexDestCoordinates][1];
                	indexDestCoordinates++;
            	}
            }

            /* set car start coordinates */
			carLatitude = 43.570630;
			carLongitude = 1.466440;
			/*listDestCoordinates[0][0] = 43.570670;
			listDestCoordinates[0][1] = 1.466460;
			listDestCoordinates[1][0] = 43.540670;
			listDestCoordinates[1][1] = 1.466400;*/

			/* movement */
			/*for (int i=0; i<nbDestCoordinates; i++) {
				carLatitudeStart = carLatitude;
				carLongitudeStart = carLongitude;
				pos_OK = 0;
				destLatitude = listDestCoordinates[i][0];
				destLongitude = listDestCoordinates[i][1];
				movement_without_GPS(carLatitudeStart, carLongitudeStart, destLatitude, destLongitude);*/
				/*if (isFire == 0) {
					turn360();
				}
				else waiting_while_not_fire();
			}*/


            /* autonomous movement to several destination with GPS connection + routine fire detection at each location */
			#else
			 /* receive coordinates of the path and store it*/
			if (latDegDes != 0) {
				if (indexDestCoordinates <= nbDestCoordinates) {
					listDestCoordinates[indexDestCoordinates][0] = dms2dd(latDegDes, latMinDes, latSecDes, latTenDes);
					listDestCoordinates[indexDestCoordinates][1] = dms2dd(lonDegDes, lonMinDes, lonSecDes, lonTenDes);
					indexDestCoordinates++;
					dest_coordinates_to_zero();
				}
			}

			/* receive car start coordinates */
			if (latDegPos != 0) {
				if (indexCarCoordinates <= nbCarCoordinates) {
					listCarCoordinates[indexCarCoordinates][0] = dms2dd(latDegPos, latMinPos, latSecPos, latTenPos);
					listCarCoordinates[indexCarCoordinates][1] = dms2dd(lonDegPos, lonMinPos, lonSecPos, lonTenPos);
					indexCarCoordinates++;
					car_coordinates_to_zero();
				}
			}

			/* calculate of the average to be more precise */
			for (int i=0; i < nbCarCoordinates; i++) {
				meanCarLatitude = meanCarLatitude + listCarCoordinates[i][0];
				meanCarLongitude = meanCarLongitude + listCarCoordinates[i][1];
			}
			carLatitude = meanCarLatitude/nbCarCoordinates;
			carLongitude = meanCarLongitude/nbCarCoordinates;

			/* movement */
			for (int i=0; i<nbDestCoordinates; i++) {
				carLatitudeStart = carLatitude;
				carLongitudeStart = carLongitude;
				pos_OK = 0;
				destLatitude = listDestCoordinates[i][0];
				destLongitude = listDestCoordinates[i][1];
				movement_without_GPS(carLatitudeStart, carLongitudeStart, destLatitude, destLongitude);
				if (isFire == 0) turn360();
				else waiting_while_not_fire();
			}

			/*destLongitude = 42.888414;
			destLatitude = 2.198709;

			if (latDegPos != 0.0) {
				if (cnt > 1000) {
					car_coordinates_to_zero();
					cnt = 0;
					car_control(50,50);
				}

				carLatitude = dms2dd(latDegPos, latMinPos, latSecPos, latTenPos);
				carLongitude = dms2dd(lonDegPos, lonMinPos, lonSecPos, lonTenPos);
				dist = get_distance(carLatitude, carLongitude, destLatitude, destLongitude);
				cnt++;

				if (carLatitudePrev == 0) {
					carLatitudePrev = carLatitude;
					carLongitudePrev = carLongitude;
					movement_with_GPS(carLatitude, carLongitude, carLatitudePrev, carLongitudePrev, destLatitude, destLongitude);
				}
				else {
					movement_with_GPS(carLatitude, carLongitude, carLatitudePrev, carLongitudePrev, destLatitude, destLongitude);
					carLatitudePrev = carLatitude;
					carLongitudePrev = carLongitude;
				}

			}*/

			#endif
        }

        /* CAN */
        // Envoi des mesures
        if (SEND_CAN) {
            SEND_CAN = 0;
            data[0] = (ADCBUF[1] >> 8) & 0xFF; // ACK chemin reçu
            data[1] = ADCBUF[1] & 0xFF;
            
            data[2] = (pos_OK>> 8) & 0xFF; // ACK position OK
            data[3] =  pos_OK & 0xFF;
            
            data[4] = (ADCBUF[0] >> 8) & 0xFF; // niveau de batterie
            data[5] = ADCBUF[0] & 0xFF;
            
            /*data[6] = (VMD_mes >> 8) & 0xFF; // VMD_mes
            data[7] = VMD_mes & 0xFF;*/
            
            CAN_Send(data, CAN_ID_MS);
        }
        
    }
    /* USER CODE END 3 */
}


/**
 * @brief System Clock Configuration
 * @retval None
 */
void SystemClock_Config(void)
{
    
    RCC_OscInitTypeDef RCC_OscInitStruct;
    RCC_ClkInitTypeDef RCC_ClkInitStruct;
    RCC_PeriphCLKInitTypeDef PeriphClkInit;
    
    /**Initializes the CPU, AHB and APB busses clocks
     */
    RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
    RCC_OscInitStruct.HSIState = RCC_HSI_ON;
    RCC_OscInitStruct.HSICalibrationValue = 16;
    RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
    RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI_DIV2;
    RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL16;
    if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
    {
        _Error_Handler(__FILE__, __LINE__);
    }
    
    /**Initializes the CPU, AHB and APB busses clocks
     */
    RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
    |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
    RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
    RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
    RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
    RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;
    
    if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
    {
        _Error_Handler(__FILE__, __LINE__);
    }
    
    PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_ADC;
    PeriphClkInit.AdcClockSelection = RCC_ADCPCLK2_DIV8;
    if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
    {
        _Error_Handler(__FILE__, __LINE__);
    }
    
    /**Configure the Systick interrupt time
     */
    HAL_SYSTICK_Config(HAL_RCC_GetHCLKFreq()/1000);
    
    /**Configure the Systick
     */
    HAL_SYSTICK_CLKSourceConfig(SYSTICK_CLKSOURCE_HCLK);
    
    /* SysTick_IRQn interrupt configuration */
    HAL_NVIC_SetPriority(SysTick_IRQn, 0, 15U);
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
 * @brief  This function is executed in case of error occurrence.
 * @param  file: The file name as string.
 * @param  line: The line in file as a number.
 * @retval None
 */
void _Error_Handler(char *file, int line)
{
    /* USER CODE BEGIN Error_Handler_Debug */
    /* User can add his own implementation to report the HAL error return state */
    /*while(1)
     {
     }*/
    /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
 * @brief  Reports the name of the source file and the source line number
 *         where the assert_param error has occurred.
 * @param  file: pointer to the source file name
 * @param  line: assert_param error line source number
 * @retval None
 */
void assert_failed(uint8_t* file, uint32_t line)
{ 
    /* USER CODE BEGIN 6 */
    /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
    /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/**
 * @}
 */

/**
 * @}
 */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
