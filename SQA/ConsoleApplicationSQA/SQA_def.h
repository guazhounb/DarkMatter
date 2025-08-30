#ifndef SQA_CONST_H
#define SQA_CONST_H

/**
 * @file sqa_const.h
 * @brief SQAЭ����ĳ�������
 * @details ͳһ����Э����صİ汾���˿ڡ����ݰ���С�Ⱥ��ĳ�����
 *          ���ں����汾���ݡ�ά��������
 */

 // Э��汾�ţ����ڰ汾����������
const int SQA_VERSION = 1;

// Ĭ�϶˿ںţ�ѡ�񲻳��ö˿��Ա����ͻ
const unsigned short SQA_DEFAULT_PORT = 7946;

// ������ݰ���С��������̫��MTU(1500�ֽ�)
const unsigned int MAX_PACKET_SIZE = 1500;

// ��ʱ�ش�ʱ�䣬��λ�����룬ƽ���ӳ���ɿ���
const unsigned int RETRANSMIT_TIMEOUT = 500;

// ������Դ�������ֹ�����ش�ռ��������Դ
const unsigned int MAX_RETRIES = 3;

#endif // SQA_CONST_H
