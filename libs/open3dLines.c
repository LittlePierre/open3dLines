struct Point3d {
double x;
double y;
double z;
};
struct Matrice3D{
	double m11;
	double m12;
	double m13;
	double m21;
	double m22;
	double m23;
	double m31;
	double m32;
	double m33;
};
struct Parameters2d{
	double scale;
	int offsetx;
	int offsety
};
struct Point2d{
	int x;
	int y;
};
struct Point3d produitMatricePoint(struct Matrice3D matrice, struct Point3d point)
{
	struct Point3d rotated;
	rotated.x =matrice.m11 * point.x+
			matrice.m12*point.y+
			matrice.m13*point.z;
	rotated.y =matrice.m21 * point.x+
			matrice.m22*point.y+
			matrice.m23*point.z;
	rotated.z =matrice.m31 * point.x+
			matrice.m32*point.y+
			matrice.m33*point.z;
	return rotated;
}
struct Point2d fastModel2View(struct Point3d point,
		struct Matrice3D RotationMatrixFromModel,
		struct Point3d Model2CamtranslationVector,
		struct Parameters2d parameters2d)
{
	struct Point3d rotated;
	rotated = produitMatricePoint(RotationMatrixFromModel,point);
	struct Point3d transvInCamView;
	transvInCamView = produitMatricePoint(RotationMatrixFromModel,Model2CamtranslationVector);

	struct Point2d translatedV;
	translatedV.x = rotated.x + transvInCamView.x;
	translatedV.y = rotated.y + transvInCamView.y;


	struct Point2d p2viewscaled;
	p2viewscaled.x =translatedV.x*parameters2d.scale + parameters2d.offsetx;
	p2viewscaled.y =-translatedV.y*parameters2d.scale + parameters2d.offsety;
	return p2viewscaled;
}




