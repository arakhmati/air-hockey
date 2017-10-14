#include "circle.h"

namespace air_hockey {

	Circle::Circle() {}

    Circle::Circle(Vector2D position,
                   float radius,
				   Vector2D borders,
				   float mass,
				   float maximum_speed,
				   float friction,
				   float body_restitution,
				   float wall_restitution) {
    	this->position = position;
    	this->radius = radius;
    	this->borders = borders;

		if (mass == 0.0)
			throw invalid_argument("Mass cannot be zero");
		this->inverse_mass = 1 / mass;

    	this->maximum_speed = maximum_speed;
    	this->friction = friction;
    	this->body_restitution = body_restitution;
    	this->wall_restitution = wall_restitution;

    	this->velocity = Vector2D(0.0f, 0.0f);
    	this->accumulated_forces = Vector2D(0.0f, 0.0f);
		this->default_position = this->position;
    }

    Circle::~Circle() { }

    void Circle::set_velocity(Vector2D velocity) {
	  float magnitude = velocity.magnitude();
	  // Limit velocity to prevent the body from escaping its borders
	  if (magnitude > this->maximum_speed)
		  velocity *= this->maximum_speed / magnitude;
	  this->velocity = velocity;
    }

    Vector2D Circle::get_velocity() {
        return this->velocity;
    }

	float Circle::get_inverse_mass() {
		return this->inverse_mass;
	}

	void Circle::add_force(Vector2D &force) {
		this->accumulated_forces += force;
	}

	void Circle::clear_accumulators() {
		this->accumulated_forces.set_to_zero();
	}

	// updates position and velocity
    void Circle::integrate() {
        Vector2D velocity = this->velocity + this->accumulated_forces * this->inverse_mass;
        velocity *= this->friction;
        this->set_velocity(velocity);
        this->position += this->velocity;
    }

	void Circle::reset() {
		this->clear_accumulators();
		this->position = this->default_position;
		this->velocity.set_to_zero();
	}


    ostream& operator<<(ostream &os, Circle const &o) {
        return os <<
        	   o.position << endl <<
			   o.radius << endl <<
			   o.borders << endl <<
			   o.inverse_mass << endl <<
			   o.maximum_speed << endl <<
			   o.friction << endl <<
			   o.body_restitution << endl <<
			   o.wall_restitution << endl <<
			   o.velocity << endl <<
			   o.accumulated_forces << endl <<
			   o.default_position << endl;
    }

	Puck::Puck(Vector2D position, float radius, Vector2D borders) :
		Circle(position,
			   radius,
			   borders,
			   puck_mass,
			   puck_maximum_speed,
			   puck_friction,
			   mallet_mallet_restitution,
			   puck_wall_restitution) {}

	Puck::~Puck() { }

	Mallet::Mallet(Vector2D position, float radius, Vector2D borders) :
		Circle(position,
			   radius,
			   borders,
			   mallet_mass,
			   mallet_maximum_speed,
			   mallet_friction,
			   puck_mallet_restitution,
			   mallet_wall_restitution) {}

	Mallet::~Mallet() { }
}


