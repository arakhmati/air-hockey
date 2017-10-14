#ifndef AIR_HOCKEY_VECTOR_H
#define AIR_HOCKEY_VECTOR_H

#include "math.h"
#include <iostream>

using namespace std;

namespace air_hockey {
    class Vector2D {

		friend ostream& operator<<(ostream &os, Vector2D const &o);

		public:
    		Vector2D();
			Vector2D(float x, float y);
			virtual ~Vector2D();

			void operator=(const Vector2D& b);
			Vector2D operator+(const Vector2D& b);
			Vector2D operator-(const Vector2D& b);
			Vector2D operator*(const Vector2D& b);
			Vector2D operator*(float factor);
			void operator+=(const Vector2D& b);
			void operator*=(float factor);

			float magnitude();
			void normalize();
			void set_to_zero();

		private:
			float x;
			float y;


    };
}
#endif
