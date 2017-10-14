#ifndef AIR_HOCKEY_CIRCLE_H
#define AIR_HOCKEY_CIRCLE_H

#include <stdexcept>
#include "vector2D.h"
#include "phy_const.h"

using namespace std;

namespace air_hockey {
    class Circle {

		friend ostream& operator<<(ostream &os, Circle const &o);

		public:
    		Circle();
			Circle(Vector2D position,
				   float radius,
				   Vector2D borders,
				   float mass,
				   float maximum_speed,
				   float friction,
				   float body_restitution,
				   float wall_restitution);
			virtual ~Circle();

			void set_velocity(Vector2D velocity);
			Vector2D get_velocity();
			float get_inverse_mass();

			void add_force(Vector2D &force);
			void clear_accumulators();

			void integrate();
			void reset();

			void print();

		private:
			Vector2D position;
			float radius;
			Vector2D borders;
			float inverse_mass;
			float maximum_speed;
			float friction;
			float body_restitution;
			float wall_restitution;
			Vector2D default_position;
			Vector2D velocity;
			Vector2D accumulated_forces;
    };

    class Puck : public Circle {
		public:
    		Puck(Vector2D position, float radius, Vector2D borders);
			virtual ~Puck();
	};

    class Mallet : public Circle {
		public:
    		Mallet(Vector2D position, float radius, Vector2D borders);
			virtual ~Mallet();
	};
}
#endif
