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
#include "stm32l4xx_hal.h"
#include "can.h"

/* User can use this section to tailor CANx instance used and associated
   resources */
/* Definition for CANx clock resources */
#define CANx                            CAN
#define CANx_CLK_ENABLE()               __HAL_RCC_CAN1_CLK_ENABLE()
#define CANx_GPIO_CLK_ENABLE()          __HAL_RCC_GPIOB_CLK_ENABLE()

#define CANx_FORCE_RESET()              __HAL_RCC_CAN1_FORCE_RESET()
#define CANx_RELEASE_RESET()            __HAL_RCC_CAN1_RELEASE_RESET()

/* Definition for CANx Pins */
#define CANx_TX_PIN                    GPIO_PIN_12
#define CANx_TX_GPIO_PORT              GPIOA
#define CANx_TX_AF                     GPIO_AF9_CAN1
#define CANx_RX_PIN                    GPIO_PIN_11
#define CANx_RX_GPIO_PORT              GPIOA
#define CANx_RX_AF                     GPIO_AF9_CAN1

/* Definition for CAN's NVIC */
#define CANx_RX_IRQn                   CAN1_RX0_IRQn
#define CANx_RX_IRQHandler             CAN1_RX0_IRQHandler

/*
 * Rx FIFO 0 filter ID definition
 */
#define FIFO_0_ID_HIGH 0x0000
#define FIFO_0_ID_LOW 0x0000
#define FIFO_0_MASK_HIGH 0x0000
#define FIFO_0_MASK_LOW 0x0000

/*
 * Local variables
 */
//static CAN_HandleTypeDef     hcan;
CAN_HandleTypeDef     hcan;
static CAN_TxHeaderTypeDef   TxHeader;
static CAN_RxHeaderTypeDef   RxHeader;
static uint8_t               TxData[8];
static uint8_t               RxData[8];
static uint32_t              TxMailbox;

static CanRxCallback rxCallback=0;

/**
 * @brief  Configures the CAN.
 * @param  None
 * @retval None
 */
void CAN_Init(void)
{
	//CAN_FilterTypeDef  sFilterConfig;

	hcan.Instance = CANx;
	hcan.Init.Prescaler = 20;
	hcan.Init.Mode = CAN_MODE_NORMAL;
	hcan.Init.SyncJumpWidth = CAN_SJW_1TQ;
	hcan.Init.TimeSeg1 = CAN_BS1_7TQ;
	hcan.Init.TimeSeg2 = CAN_BS2_2TQ;
	hcan.Init.TimeTriggeredMode = DISABLE;
	hcan.Init.AutoBusOff = ENABLE;
	hcan.Init.AutoWakeUp = DISABLE;
	hcan.Init.AutoRetransmission = DISABLE;
	hcan.Init.ReceiveFifoLocked = DISABLE;
	hcan.Init.TransmitFifoPriority = DISABLE;

	if (HAL_CAN_Init(&hcan) != HAL_OK)
	{
		while(1);
	}

	/*##-2- Configure the CAN Filter ###########################################*/
	/*sFilterConfig.FilterBank = 0;
	sFilterConfig.FilterMode = CAN_FILTERMODE_IDMASK;
	sFilterConfig.FilterScale = CAN_FILTERSCALE_32BIT;
	sFilterConfig.FilterIdHigh = FIFO_0_ID_HIGH;
	sFilterConfig.FilterIdLow = FIFO_0_ID_LOW;
	sFilterConfig.FilterMaskIdHigh = FIFO_0_MASK_HIGH;
	sFilterConfig.FilterMaskIdLow = FIFO_0_MASK_LOW;
	sFilterConfig.FilterFIFOAssignment = CAN_RX_FIFO0;
	sFilterConfig.FilterActivation = ENABLE;
	sFilterConfig.SlaveStartFilterBank = 14;

	if (HAL_CAN_ConfigFilter(&hcan, &sFilterConfig) != HAL_OK)
	{
		while (1);
	}*/

	/*##-3- Start the CAN peripheral ###########################################*/
	if (HAL_CAN_Start(&hcan) != HAL_OK)
	{
		while (1);
	}

	/*##-4- Activate CAN RX notification #######################################*/
	if (HAL_CAN_ActivateNotification(&hcan, CAN_IT_RX_FIFO0_MSG_PENDING) != HAL_OK)
	{
		while (1);
	}
}

/**
 * @brief CAN MSP Initialization
 *        This function configures the hardware resources used in this example:
 *           - Peripheral's clock enable
 *           - Peripheral's GPIO Configuration
 *           - NVIC configuration for DMA interrupt request enable
 * @param hcan: CAN handle pointer
 * @retval None
 */
void HAL_CAN_MspInit(CAN_HandleTypeDef *hcan)
{
	GPIO_InitTypeDef   GPIO_InitStruct;

	/*##-1- Enable peripherals and GPIO Clocks #################################*/
	/* CAN1 Periph clock enable */
	CANx_CLK_ENABLE();
	/* Enable GPIO clock ****************************************/
	CANx_GPIO_CLK_ENABLE();

	/*##-2- Configure peripheral GPIO ##########################################*/
	/* CAN1 TX GPIO pin configuration */
	GPIO_InitStruct.Pin = CANx_TX_PIN;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Pull = GPIO_PULLUP;
	GPIO_InitStruct.Alternate =  CANx_TX_AF;

	HAL_GPIO_Init(CANx_TX_GPIO_PORT, &GPIO_InitStruct);

	/* CAN1 RX GPIO pin configuration */
	GPIO_InitStruct.Pin = CANx_RX_PIN;
	GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
	GPIO_InitStruct.Pull = GPIO_PULLUP;
	GPIO_InitStruct.Alternate =  CANx_RX_AF;

	HAL_GPIO_Init(CANx_RX_GPIO_PORT, &GPIO_InitStruct);

	/*##-3- Configure the NVIC #################################################*/
	/* NVIC configuration for CAN1 Reception complete interrupt */
	HAL_NVIC_SetPriority(CANx_RX_IRQn, 15, 0);
	HAL_NVIC_EnableIRQ(CANx_RX_IRQn);
}

/**
 * @brief CAN MSP De-Initialization
 *        This function frees the hardware resources used in this example:
 *          - Disable the Peripheral's clock
 *          - Revert GPIO to their default state
 * @param hcan: CAN handle pointer
 * @retval None
 */
void HAL_CAN_MspDeInit(CAN_HandleTypeDef *hcan)
{
	/*##-1- Reset peripherals ##################################################*/
	CANx_FORCE_RESET();
	CANx_RELEASE_RESET();

	/*##-2- Disable peripherals and GPIO Clocks ################################*/
	/* De-initialize the CAN1 TX GPIO pin */
	HAL_GPIO_DeInit(CANx_TX_GPIO_PORT, CANx_TX_PIN);
	/* De-initialize the CAN1 RX GPIO pin */
	HAL_GPIO_DeInit(CANx_RX_GPIO_PORT, CANx_RX_PIN);

	/*##-4- Disable the NVIC for CAN reception #################################*/
	HAL_NVIC_DisableIRQ(CANx_RX_IRQn);
}

/**
 * @brief CAN MSP De-Initialization
 *        This function frees the hardware resources used in this example:
 *          - Disable the Peripheral's clock
 *          - Revert GPIO to their default state
 * @param hcan: CAN handle pointer
 * @retval None
 */
/*void CAN_Send(uint8_t std_id, uint8_t ext_id, uint8_t len, uint8_t data[])
{*/
	/* Configure Transmission header */
/*	TxHeader.StdId = std_id;
	TxHeader.ExtId = ext_id;
	TxHeader.RTR = CAN_RTR_DATA;
	TxHeader.IDE = CAN_ID_STD;
	TxHeader.DLC = len;
	TxHeader.TransmitGlobalTime = DISABLE;*/

	/* Set the data to be transmitted */
/*	for(int i=0; i < len; i++)
		TxData[i] = data[i];
*/
	/* Start the Transmission process */
/*	if (HAL_CAN_AddTxMessage(&hcan, &TxHeader, TxData, &TxMailbox) != HAL_OK)
	{
*/		/* Transmission request Error */
/*		while (1);
	}
	HAL_Delay(10);
}*/

void CAN_Send(uint8_t* data, uint32_t id)
{
	TxHeader.StdId = id;
	TxHeader.ExtId = 0;
	TxHeader.RTR = CAN_RTR_DATA;
	TxHeader.IDE = CAN_ID_STD;
	TxHeader.DLC = 8;
	TxHeader.TransmitGlobalTime = DISABLE;

	for(int i=0; i < 8; i++)
		TxData[i] = data[i];

	/* Start the Transmission process */
		if (HAL_CAN_AddTxMessage(&hcan, &TxHeader, TxData, &TxMailbox) != HAL_OK)
		{
			/* Transmission request Error */
			while (1);
		}
		HAL_Delay(10);
}


void CAN_AddRXCallback(CanRxCallback callback)
{
	rxCallback = callback;
}

/**
 * @brief  Rx Fifo 0 message pending callback
 * @param  hcan: pointer to a CAN_HandleTypeDef structure that contains
 *         the configuration information for the specified CAN.
 * @retval None
 */
void HAL_CAN_RxFifo0MsgPendingCallback(CAN_HandleTypeDef *hcan)
{
	/* Get RX message */
	if (HAL_CAN_GetRxMessage(hcan, CAN_RX_FIFO0, &RxHeader, RxData) != HAL_OK)
	{
		while (1);
	}

	if (rxCallback!=0) rxCallback(&RxHeader,RxData);
}

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
