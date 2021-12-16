/**
  ******************************************************************************
  * File Name          : CAN.c
  * Description        : This file provides code for the configuration
  *                      of the CAN instances.
  ******************************************************************************
  ** This notice applies to any and all portions of this file
  * that are not between comment pairs USER CODE BEGIN and
  * USER CODE END. Other portions of this file, whether 
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
#include "can.h"

#include "gpio.h"

/* USER CODE BEGIN 0 */

extern int cmdLRM, cmdRRM, cmdSFM, cmdPOS;
extern GPIO_PinState en_MARG, en_MARD, en_MAV, en_POS;

extern int modeSpeed;
extern int modeSteer;

/* USER CODE END 0 */

CAN_HandleTypeDef hcan;

/* CAN init function */
void MX_CAN_Init(void)
{
  hcan.Instance = CAN1;
  hcan.Init.Prescaler = 8;
  hcan.Init.Mode = CAN_MODE_NORMAL;
  hcan.Init.SJW = CAN_SJW_1TQ;
  hcan.Init.BS1 = CAN_BS1_7TQ;
  hcan.Init.BS2 = CAN_BS2_2TQ;
  hcan.Init.TTCM = DISABLE;
  hcan.Init.ABOM = DISABLE;
  hcan.Init.AWUM = DISABLE;
  hcan.Init.NART = DISABLE;
  hcan.Init.RFLM = DISABLE;
  hcan.Init.TXFP = DISABLE;
  if (HAL_CAN_Init(&hcan) != HAL_OK)
  {
    _Error_Handler(__FILE__, __LINE__);
  }

  CAN_FilterConfig();

  __HAL_CAN_ENABLE_IT(&hcan, CAN_IT_FMP0);
}

void HAL_CAN_MspInit(CAN_HandleTypeDef* canHandle)
{

  GPIO_InitTypeDef GPIO_InitStruct;
  if(canHandle->Instance==CAN1)
  {
  /* USER CODE BEGIN CAN1_MspInit 0 */

  /* USER CODE END CAN1_MspInit 0 */
    /* CAN1 clock enable */
    __HAL_RCC_CAN1_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();

    /**CAN GPIO Configuration    
    PA11     ------> CAN_RX
    PA12     ------> CAN_TX 
    */
    GPIO_InitStruct.Pin = GPIO_PIN_11;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

    GPIO_InitStruct.Pin = GPIO_PIN_12;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

    /* CAN1 interrupt Init */
    HAL_NVIC_SetPriority(USB_LP_CAN1_RX0_IRQn, 0, 1U);
    HAL_NVIC_EnableIRQ(USB_LP_CAN1_RX0_IRQn);
  /* USER CODE BEGIN CAN1_MspInit 1 */

  /* USER CODE END CAN1_MspInit 1 */
  }
}

void HAL_CAN_MspDeInit(CAN_HandleTypeDef* canHandle)
{

  if(canHandle->Instance==CAN1)
  {
  /* USER CODE BEGIN CAN1_MspDeInit 0 */

  /* USER CODE END CAN1_MspDeInit 0 */
    /* Peripheral clock disable */
    __HAL_RCC_CAN1_CLK_DISABLE();


    /**CAN GPIO Configuration    
    PA11     ------> CAN_RX
    PA12     ------> CAN_TX 
    */
    HAL_GPIO_DeInit(GPIOA, GPIO_PIN_11|GPIO_PIN_12);

    /* CAN1 interrupt Deinit */
    HAL_NVIC_DisableIRQ(USB_LP_CAN1_RX0_IRQn);
  /* USER CODE BEGIN CAN1_MspDeInit 1 */

  /* USER CODE END CAN1_MspDeInit 1 */
  }
} 

/* USER CODE BEGIN 1 */

void CAN_FilterConfig(void)
{
	CAN_FilterConfTypeDef sFilterConfig;	
	
	sFilterConfig.FilterNumber = 0;
	sFilterConfig.FilterMode = CAN_FILTERMODE_IDLIST;
	sFilterConfig.FilterScale = CAN_FILTERSCALE_16BIT;
	sFilterConfig.FilterIdHigh = CAN_ID_CMC<<5;
	sFilterConfig.FilterIdLow = CAN_ID_SSC<<5;
	//sFilterConfig.FilterMaskIdHigh = 0xFFFF;
	//sFilterConfig.FilterMaskIdLow = 0xFFFF;
	sFilterConfig.FilterFIFOAssignment = CAN_FILTER_FIFO0;
	sFilterConfig.FilterActivation = ENABLE;
	sFilterConfig.BankNumber = 14;
	
	if( HAL_CAN_ConfigFilter(&hcan, &sFilterConfig) != HAL_OK )
	{
		_Error_Handler(__FILE__, __LINE__);
	}
}


void CAN_Send(uint8_t* data, uint32_t id)
{		
	hcan.pTxMsg->StdId = id;
	hcan.pTxMsg->RTR = CAN_RTR_DATA;
	hcan.pTxMsg->IDE = CAN_ID_STD;
	hcan.pTxMsg->DLC = 8;
		
	for(int i=0; i < 8; i++)
		hcan.pTxMsg->Data[i] = data[i];
	
		
	if( HAL_CAN_Transmit(&hcan, 10) != HAL_OK )
	{
		Error_Handler();
	}
}


int read_cmd(uint8_t data, GPIO_PinState *en_M)
{
	uint8_t tmp;
	uint8_t VMdata;

	tmp= data>>7;
	if (tmp!=0) *en_M=GPIO_PIN_SET;
	else *en_M=GPIO_PIN_RESET;

	VMdata = data & 0x7F;
	return (int)VMdata;
}

int read_mode(uint8_t data) //En soit cette fonction ne sert a rien parce qu'on pourrait simplement recuperer la data en la typecastant int
{
	uint8_t VMdata;

	VMdata = data & 0xFF; //On recupere ici les 8 bits (l'encodage du MODE se fait sur les 8 bits)
	return (int)VMdata;
}

void HAL_CAN_RxCpltCallback(CAN_HandleTypeDef* hcan)
{
	
	/* Consigne vitesse moteur */
	if(hcan->pRxMsg->StdId == CAN_ID_CMC)
	{
		cmdLRM = read_cmd(hcan->pRxMsg->Data[0], &en_MARG);
		cmdRRM = read_cmd(hcan->pRxMsg->Data[1], &en_MARD);
		cmdSFM = read_cmd(hcan->pRxMsg->Data[2], &en_MAV);
		cmdPOS = read_cmd(hcan->pRxMsg->Data[3], &en_POS);
	}

	/* Consigne vitesse et direction */
	if(hcan->pRxMsg->StdId == CAN_ID_SSC)
	{
		modeSpeed = read_mode(hcan->pRxMsg->Data[0]);
		modeSteer = read_mode(hcan->pRxMsg->Data[1]);
	}
		
	__HAL_CAN_ENABLE_IT(hcan, CAN_IT_FMP0);
}
/* USER CODE END 1 */

/**
  * @}
  */

/**
  * @}
  */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
