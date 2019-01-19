int main()
{
        int i = 1;
        int sum = 0;
        sum = i;
        int j;
        switch(sum+i){
            case 0:
                sum *= 2;
                i++;
                break;
            case 1:
                sum = i+5;
                i *= 2;
                break;
            case 2:
                sum -= 2;
                i--;
                break;
            default:
                sum = 0;
                i = 0;
                break;
        }

        return 0;
}