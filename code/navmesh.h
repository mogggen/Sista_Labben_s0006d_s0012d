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
    static Math::vec3 getCenterOfFace(int face);
    static bool isInTriangle(Math::vec2 p, int face);
    static bool isInFace(Math::vec2 p, int face);
    static bool isOnNavMesh(Math::vec2 p);
    static int findInNavMesh(Math::vec2 p);
    static int findInNavMeshIndex(Math::vec2 p);
     
private:
    Util::Array<Math::vec3> verticies;
    Util::Array<int> faces;
    Util::Array<HalfEdge> halfEdgeArray;
};

} // End namespace Demo


#endif /* NAVMESH_H */
