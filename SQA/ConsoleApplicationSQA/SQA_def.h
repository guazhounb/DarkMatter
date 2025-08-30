#ifndef SQA_CONST_H
#define SQA_CONST_H

/**
 * @file sqa_const.h
 * @brief SQA协议核心常量定义
 * @details 统一管理协议相关的版本、端口、数据包大小等核心常量，
 *          便于后续版本兼容、维护和升级
 */

 // 协议版本号，用于版本兼容与升级
const int SQA_VERSION = 1;

// 默认端口号，选择不常用端口以避免冲突
const unsigned short SQA_DEFAULT_PORT = 7946;

// 最大数据包大小，适配以太网MTU(1500字节)
const unsigned int MAX_PACKET_SIZE = 1500;

// 超时重传时间，单位：毫秒，平衡延迟与可靠性
const unsigned int RETRANSMIT_TIMEOUT = 500;

// 最大重试次数，防止无限重传占用网络资源
const unsigned int MAX_RETRIES = 3;

#endif // SQA_CONST_H
