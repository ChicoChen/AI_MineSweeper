// MineSweeper.cpp : 此檔案包含 'main' 函式。程式會於該處開始執行及結束執行。
//

#include "MineSweeper.h"

#include <iostream>
#include <string>
#include <sstream>

using namespace std;

int main(){
    MineSweeper game;
    game.show(true);

    string input;
    int x, y;
    char action = NULL;
    int step = 0;
    while (getline(cin, input)) {
        stringstream sin;
        sin.str(input);

        sin >> x;
        sin >> y;
        sin >> action;
        //cout << bool(action) << endl;
        step += 1;
        
        //nextstep();
        //display();
        bool flag = game.step(x, y, action);
        cout << "step: " << step << endl;
        game.show(true);
        if (!flag) {
            cout << "Gameover :(" << endl;
            break;
        }
        else if (game.endCheck()) {
            cout << "we win :)" << endl;
            game.show(false);
            break;
        }
        action = NULL;
    }
}

// 執行程式: Ctrl + F5 或 [偵錯] > [啟動但不偵錯] 功能表
// 偵錯程式: F5 或 [偵錯] > [啟動偵錯] 功能表

// 開始使用的提示: 
//   1. 使用 [方案總管] 視窗，新增/管理檔案
//   2. 使用 [Team Explorer] 視窗，連線到原始檔控制
//   3. 使用 [輸出] 視窗，參閱組建輸出與其他訊息
//   4. 使用 [錯誤清單] 視窗，檢視錯誤
//   5. 前往 [專案] > [新增項目]，建立新的程式碼檔案，或是前往 [專案] > [新增現有項目]，將現有程式碼檔案新增至專案
//   6. 之後要再次開啟此專案時，請前往 [檔案] > [開啟] > [專案]，然後選取 .sln 檔案
