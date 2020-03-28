#include <string>
#include <fstream>
#include <math.h>

using namespace std;

long long int get_sum_seg(long long int array[], long int ind_l, long int ind_r) {
    long long int result = 0;
    while(ind_l <= ind_r) {
        if(ind_l % 2 == 1) {
            result += array[ind_l];
        }
        if(ind_r % 2 == 0) {
            result += array[ind_r];
        }
        ind_l = (ind_l + 1) / 2;
        ind_r = (ind_r - 1) / 2;
    }
    return result;
}

int main() {

    string path_in = "sum.in";
    string path_out = "sum.out";
    ifstream fin;
    ofstream fout;
    fin.open(path_in);
    fout.open(path_out);

    string operation;
    long int N, K, i, x, l, r;

    fin >> N >> K;
    long int shift = pow(2, ceil(log2(N)));
    long long int array[2*shift] = {};

    for(long int k = 0; k < K; ++k) {

        fin >> operation;

        if (operation == "A") {
            fin >> i >> x;
            i += shift - 1;
            long int diff = x - array[i];
            if (diff != 0) {
                array[i] = x;
                while (i != 1) {
                    array[i/2] += diff;
                    i /= 2;
                }
            }
        }
        
        if (operation == "Q") {
            fin >> l >> r;
            fout << get_sum_seg(array, l+shift-1, r+shift-1) << endl;
        }
    }

    fin.close();
    fout.close();
    return 0;
}
