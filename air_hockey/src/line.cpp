#include "line.h"

namespace air_hockey {

	Line::Line() {
    	this->p1 = Vector2D();
    	this->p2 = Vector2D();
	}

	Line::Line(Vector2D p1, Vector2D p2) {
    	this->p1 = p1;
    	this->p2 = p2;

    	this->direction = (this->p2 - this->p1).normalize();
		this->normal = Vector2D(this->direction.get_y(), -this->direction.get_x());
    }

	Line::~Line() { }

    ostream& operator<<(ostream &os, Line const &o) {
        return os <<
        	   o.p1 << endl <<
			   o.p2 << endl;
    }

    vector< Vector2D > generate_bezier_curve() {


    	return NULL;
    }

}



//@staticmethod
//    def generate_bezier_curve(arc_points, bezier_ratio=0.01):
//        if len(arc_points) != 3:
//            raise ValueError('Bezier curve can be generated only using 3 points')
//
//        arc_points = [np.array(point, dtype=np.float32) for point in arc_points]
//        p0, p1, p2 = arc_points
//
//#        # Make sure points are counter-clockwise
//#        sum_over_edges  = Line._edge_sum(p0, p1)
//#        sum_over_edges += Line._edge_sum(p1, p2)
//#        sum_over_edges += Line._edge_sum(p2, p0)
//#        if sum_over_edges < 0: # Points are clockwise
//#            p0, p2 = p2, p0 # Swap end points to make them counter-clockwise
//
//        points = []
//        # Generate Bezier
//        for ratio in np.arange(0.0, 1.0, bezier_ratio):
//            distance = (p1 - p0)
//            np0 = p0 + distance * ratio
//            distance = (p2 - p1)
//            np1 = p1 + distance * ratio
//            points.append(np0 + (np1 - np0) * ratio)
//        points.append(p2)
//
//        lines = []
//        for i in range(len(points)-1):
//            lines.append(Line(points[i], points[i+1]))
//
//        return lines
