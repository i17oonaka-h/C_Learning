#include <stdio.h>


int main(){
    unsigned char age = 25;
    double height = 166.7;
    float weight = 58.5;
    int num[] = {1,2,3};
    char str[] = "chara";
    double* p = &height;

    printf("年齢：%d歳\n",age);
    printf("身長：%fcm\n",height);
    printf("体重：%fkg\n",weight);

    age = 21;
    height = 152.1;

    return 0;
}