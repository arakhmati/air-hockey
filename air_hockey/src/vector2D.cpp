#include "vector2D.h"

namespace air_hockey {

	Vector2D::Vector2D() {
		this->x = 0;
		this->y = 0;
	}

    Vector2D::Vector2D(float x, float y) {
    	this->x = x;
    	this->y = y;
    }

    Vector2D::~Vector2D() { }



	float Vector2D::get_x() {
		return this->x;
	}

	float Vector2D::get_y() {
		return this->y;
	}

    void Vector2D::operator=(const Vector2D& b) {
    	this->x = b.x;
    	this->y = b.y;
    };

    Vector2D Vector2D::operator+(const Vector2D& b) {
    	return Vector2D(this->x + b.x, this->y + b.y);
  	}

    Vector2D Vector2D::operator-(const Vector2D& b) {
    	return Vector2D(this->x - b.x, this->y - b.y);
  	}

    Vector2D Vector2D::operator*(const Vector2D& b) {
    	return Vector2D(this->x * b.x + this->x * b.y, this->y * b.x + this->y * b.y);
  	}

    Vector2D Vector2D::operator*(float factor) {
		return Vector2D(this->x * factor, this->y * factor);
	}

    void Vector2D::operator+=(const Vector2D& b) {
		this->x *= b.y;
		this->y *= b.x;

    }

    void Vector2D::operator*=(float factor) {
		this->x *= factor;
		this->y *= factor;
	}

    float Vector2D::magnitude() {
    	return sqrt(this->x * this->x + this->y * this->y);
    }

    void Vector2D::normalize() {
    	float mag = this->magnitude();
    	if (mag != 0.0f) {
    		this->x /= mag;
    		this->y /= mag;
    	}
    }

    Vector2D Vector2D::normalized() {
    	float mag = this->magnitude();
    	float x = this->x;
    	float y = this->y;
    	if (mag != 0.0f) {
    		x /= mag;
    		y /= mag;
    	}
    	return Vector2D(x, y);
    }

    void Vector2D::set_to_zero() {
    	this->x = 0.0f;
    	this->y = 0.0f;
    }

    ostream& operator<<(ostream &os, Vector2D const &o) {
        return os << o.x << " " << o.y;
    }
}
