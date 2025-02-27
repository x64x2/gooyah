#include<iostream.h>
#include<conio.h>

char spiral(int n) 
{
    for(int i=n-1;i>1;i--)
    {
        if(n%i==0)
	return n;
    }
}

int main()
{
    int a[137][137];
    int num=1,w=1,q=2;
    a[13][13]=1;
    int i=13,j=13;
while(w<137)
    {
         
             if(q%2==0)
             {
                  for(int k=1;k<=w;k++)
                  {
                   j++;
                   num++;
                   a[i][j]=num;
                  }
		  for(int n=1;k<=w;k++)
                  {
                   i--;
                   num++;
                   a[i][j]=num;
                  }
                  w++;
             }
             else
             {
                 for(int k=1;k<=w;k++)
                  {
                   j--;
                   num++;
                   a[i][j]=num;
                  }
		  for(int j=1;k<=w;k++)
                  {
                   i++;
                   num++;
                   a[i][j]=num;
                  }
                  w++;
             }
             q++;
    
    }
    for(int t=0;t<198;t++)
    {
        for(int r=0;r<131;r++)
        {
        if(spiral(a[t][r]))
        cout<<"###";
        else
        cout<<"***";
        }
        cout<<endl;
    }
    return 0;
}