int sum_of(int i, int sum){
    int m;
    m = sum+i;
    m = m + 1;
    return m;
}

int sum_of222(int i, int sum){
    int j;
    j = sum+i;
    j = j + 1;
    return j;
}

int main()
{
        int i = 1;
        int sum = 0;
        sum = sum_of222(i, sum);

        return 0;
}