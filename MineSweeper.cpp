#include "MineSweeper.h"
#include <random>
#include <iostream>
#include <string>
#include <array>
#include <queue>
random_device rd;
mt19937 gen(rd());

int random(int low, int high){
	uniform_int_distribution<> dist(low, high);
	return dist(gen);
}

MineSweeper::MineSweeper(){
	this->size = 16;
	board = new char* [size];
	mask = new bool* [size];
	flags = new char* [size];
	for (int i = 0; i < size; i++) {
		board[i] = new char[16]();
		flags[i] = new char[16]();
		for (int j = 0; j < size; j++) {
			board[i][j] = '0';
		}
		mask[i] = new bool[16]();
	}

	while(mines.size() < 40){
		pair<int, int> mine = { random(0, 15), random(0, 15) };
		mines.insert(mine);
		board[mine.first][mine.second] = '@';
	}

	initialize();
}

MineSweeper::~MineSweeper() {
	for (int i = 0; i < this->size; i++) {
		delete[] board[i];
		delete[] mask[i];
	}
	delete[] board;
	delete[] mask;
}

void MineSweeper::initialize() {
	for (auto iter = mines.begin(); iter != mines.end(); iter++) {
		for (int x = -1; x <= 1; x++) {
			for (int y = -1; y <= 1; y++) {
				if (!x && !y) { continue; }
				int cor_x = iter->first + x;
				int cor_y = iter->second + y;
				
				if(cor_x < 0 || cor_x >= size){ continue; }
				else if (cor_y < 0 || cor_y >= size) { continue; }

				if (board[cor_x][cor_y] != '@') { board[cor_x][cor_y] += 1; }
			}
		}
	}
}

void MineSweeper::show(bool hide) {
	cout << string(33, '-') << endl;
	for (int i = 0; i < this->size; i++) {
		cout << '|';
		for (int j = 0; j < this->size; j++) {
			if (hide) {
				if (mask[i][j]) {
					if (board[i][j] == '0') { cout << ' ' << '|'; }
					else { cout << board[i][j] << '|'; }
				}
				else if(flags[i][j] == NULL){ cout << '#' << "|"; }
				else { cout << flags[i][j] << "|"; }
			}

			else {
				if (board[i][j] == '0') { cout << ' ' << '|'; }
				else { cout << board[i][j] << '|'; }
			}
		}
		cout << endl;
	}
	cout << string(33, '-') << endl << endl;
}

bool MineSweeper::step(int x, int y, char act) {
	if (min(x, y) < 0 || max(x, y) >= size) { // index out of bound
		cout << "!step out of gameboard! reject input" << endl;
		return true;
	}else if(mask[x][y]){ // explored block
		cout << "!redundant step!" << endl;
		return true;
	}else if (act) { // special action
		switch (act) {
		case 'F':
			flags[x][y] = 'F';
			break;
		case '?':
			flags[x][y] = '?';
			break;
		case 'C':
			flags[x][y] = NULL;
			break;
		default:
			cout << "!unexpected input!" << endl;
			break;
		}
		return true;
	}else if (flags[x][y]) { // foolproof
		cout << "!clear the flag before explore!" << endl;
		return true;
	}

	// bfs
	queue<pair<int, int>> Q;
	Q.emplace(x, y);
	while(!Q.empty()){
		pair<int, int> pos = Q.front();
		Q.pop();
		mask[pos.first][pos.second] = true;
		if (board[pos.first][pos.second] == '0') {
			for (int a = -1; a <= 1; a++) {
				for (int b = -1; b <= 1; b++) {
					int cor_x = pos.first + a;
					int cor_y = pos.second+ b;
					if (min(cor_x, cor_y) < 0 || max(cor_x, cor_y) >= size) { continue; }
					if (!mask[cor_x][cor_y] && !flags[cor_x][cor_y]) {
						mask[cor_x][cor_y] = true;
						Q.emplace(cor_x, cor_y);
					}
				}
			}
		}
	}

	for(auto iter: mines){ // step on the mine, game over
		if (iter == make_pair(x, y)) { return false;}
	}

	return true;
}

bool MineSweeper::endCheck() {
	int count = 0;
	for (int i = 0; i < size; i++) {
		for (int j = 0; j < size; j++) {
			if (!mask[i][j]) { count++; }
		}
	}

	if (count == 40) { return true; }
	else { return false; }
}