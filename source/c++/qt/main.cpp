#include <iostream>
#include <bitset>
using namespace std; //
extern int data; // extern: ȫ�ֱ���Ԥ����

// ����������
int add(int a, int b){
    cout << "��������: "; // �ַ���������\0��Ϊ�������, �������
    int data1;
    int data2;
    cin >> data >> data1 >> data2;
    // cin: �������豸��ȡ����, �����������������ת��, ��˳���ȡ, �����Կո�ָ�
    // cout: ���, endl: ���뻻�з�

    return  data + a+ b;
}
int data = 3;

// ����ռ�ÿռ�
int helpSizeOf(){
    cout << sizeof(3.14f) << endl; // float
    cout << sizeof(3.14) << endl; //double
    cout << sizeof(3) << endl; // int
    cout << sizeof(float) << endl;
    cout << sizeof(double) << endl;
    cout << sizeof(int) << endl;
    cout << sizeof(short) << endl;
    cout << sizeof(long) << endl;
    return 0 ;
}
int helpBitSet(){
cout << bitset<16>(-10) << endl; // ��ʾ������ֵ�洢ֵ, �����Բ�����ʽ�洢
cout << bitset<16>(10) << endl; // ��ʾ������ֵ�洢ֵ, ������ԭ����ʽ�洢(����ԭ���벹��һ��)
return 0;
}
int helpConst(){
    const int data = 0; // const: ֻ�ܳ�ʼ��, ���ܸ�ֵ
    cout << data << endl;
    return 0;
}
// ������
int helpRegister(){
    register int data  = 0; // ��������������cpu�Ĵ�����, c++17������������
    cout << data << endl;
    return 0;
}
int helpVolatile(){
    volatile int data = 0; // ��ֹ�������������cpu�Ĵ�����
    cout << data << endl;
    return  0;
}
int helpTypeOf(){
    typedef int INT32; // �������ͱ���
    INT32 data = 0;
    cout << data << endl;
    return  0;
}
int main()
{
//    unsigned int num1 = 1; // unsigned: �޷������ֱ�����������
//    add(num1,2);
    helpSizeOf();
//    helpBitSet();
//    helpConst();
//    helpVolatile();
    return 0;
}
