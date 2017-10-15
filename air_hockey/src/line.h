#ifndef AIR_HOCKEY_CIRCLE_H
#define AIR_HOCKEY_CIRCLE_H

#include "vector"
#include "vector2D.h"

using namespace std;

namespace air_hockey {
    class Line {

		friend ostream& operator<<(ostream &os, Line const &o);

		public:
			Line();
			Line(Vector2D p1, Vector2D p2);
			virtual ~Line();

		private:
			Vector2D p1;
			Vector2D p2;
			Vector2D normal;
			Vector2D direction;
    };
}
#endif
