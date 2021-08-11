#include <stdio.h>

// 代入文とかのテスト

int main(){
    unsigned char age = 25;
    double height = 166.7;
    float weight = 58.5;

    printf("年齢：%d歳\n",age);
    printf("身長：%fcm\n",height);
    printf("体重：%fkg\n",weight);

    age = 20;
    float a = 20.0;
    height = 175.5;
    weight = 67.2+a;

    printf("年齢：%d歳\n",age);
    printf("身長：%fcm\n",height);
    printf("体重：%fkg\n",weight);

    return 0;
}