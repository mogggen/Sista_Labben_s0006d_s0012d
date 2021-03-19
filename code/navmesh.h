#ifndef NAVMESH_H
#define NAVMESH_H 

#include "core/refcounted.h"
#include "core/singleton.h"
#include "coregraphics/legacy/nvx2streamreader.h"

namespace Demo
{
    struct HalfEdge {
        int vertIdx;
        int nextEdge;
        int neighbourEdge;
        int face;
    };
class NavMesh
{
    __DeclareSingleton(NavMesh);
public:

    static void Init();
    void Load(const char* filename);
    void DbgDraw();
    void recDraw(int edge, int recDepth);
    static int getFace(int num);
    static Math::vec3 getVertex(int num);
    static HalfEdge getHalfEdge(int num);
    static int getNumFace();
    static int getNumVertex();
    static int getNumHalfEdge();
    static Math::vec3 getCenter(int face);
     
private:
    Util::Array<Math::vec3> verticies;
    Util::Array<int> faces;
    Util::Array<HalfEdge> halfEdgeArray;
};

} // End namespace Demo


#endif /* NAVMESH_H */
