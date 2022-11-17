#include <iostream>
#include <bitset>
using namespace std; //
extern int data; // extern: 全局变量预声明

// 加上连个数
int add(int a, int b){
    cout << "输入数字: "; // 字符串常量以\0作为结束标记, 方便遍历
    int data1;
    int data2;
    cin >> data >> data1 >> data2;
    // cin: 从输入设备获取输入, 会根据数据类型自行转换, 按顺序获取, 或者以空格分割
    // cout: 输出, endl: 插入换行符

    return  data + a+ b;
}
int data = 3;

// 数据占用空间
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
cout << bitset<16>(-10) << endl; // 显示二进制值存储值, 负数以补码形式存储
cout << bitset<16>(10) << endl; // 显示二进制值存储值, 正数以原码形式存储(正数原码与补码一致)
return 0;
}
int helpConst(){
    const int data = 0; // const: 只能初始化, 不能赋值
    cout << data << endl;
    return 0;
}
// 主函数
int helpRegister(){
    register int data  = 0; // 主动将变量放入cpu寄存器中, c++17将此特性弃用
    cout << data << endl;
    return 0;
}
int helpVolatile(){
    volatile int data = 0; // 禁止将这个变量放入cpu寄存器中
    cout << data << endl;
    return  0;
}
int helpTypeOf(){
    typedef int INT32; // 设置类型别名
    INT32 data = 0;
    cout << data << endl;
    return  0;
}
int main()
{
//    unsigned int num1 = 1; // unsigned: 无符号数字必须特殊声明
//    add(num1,2);
    helpSizeOf();
//    helpBitSet();
//    helpConst();
//    helpVolatile();
    return 0;
}
