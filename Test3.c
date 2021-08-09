#include <stdio.h>

// 20行以上のプログラムを上手く管理できるかテスト．

int main(){
    unsigned char age = 25;
    double height = 166.7;
    float weight = 58.5;

    printf("年齢：%d歳\n",age);
    printf("身長：%fcm\n",height);
    printf("体重：%fkg\n",weight);

    age = 21;
    height = 152.1;

    return 0;
}