#ifndef MINESWEEPER
#define	MINESWEEPER

#include <set>
using namespace std;
class MineSweeper
{
private:
	int size;
	int num_mines;
	char** board;
	bool** mask;
	char** flags;
	set<pair<int, int>> mines;

public:

	MineSweeper();
	~MineSweeper();
	void initialize();
	void show(bool hide);
	bool step(int x, int y, char act);
	bool endCheck();
};
#endif


