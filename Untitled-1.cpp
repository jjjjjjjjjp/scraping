#include <iostream>
#include <random>
#include <iomanip>

using std::cout;
using std::endl;
using std::setprecision;

// Modify as needed
constexpr int MIN_X = 34.68;
constexpr int MIN_Y = 37.028;
constexpr int MAX_X = 137.48;
constexpr int MAX_Y = 137.48;

int main()
{
    std::random_device rd;
    std::default_random_engine eng(rd());
    std::uniform_real_distribution<double> distr_X(MIN_X, MAX_X);
    std::uniform_real_distribution<double> distr_Y(MIN_Y, MAX_Y);

    for (int n = 0; n < 1; ++n) {
        cout << setprecision(10)
             << distr_X(eng) << "," << distr_Y(eng) << "\n";
    }
    cout << endl;

    return EXIT_SUCCESS;
}