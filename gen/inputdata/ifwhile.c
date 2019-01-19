int main()
{
        int i = 0;
        int sum = i+1;
        while(i<10){
            i += sum;
            i++;
        }
        if(sum>=0){
            int j;
            j = i*2;
            sum += j;
        }
        else{
            while(sum>0){
                sum += i;
                i = i+1;
            }
            i *= 2;
        }

        return 0;
}