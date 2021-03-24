#include "application/stdneb.h"
#include "navmesh.h"

#include "core/refcounted.h"
#include "models/modelcontext.h"
#include "graphics/graphicsentity.h"
#include "visibility/visibilitycontext.h"
#include "graphicsfeature/graphicsfeatureunit.h"
#include "basegamefeature/managers/entitymanager.h"
#include "basegamefeature/properties/transform.h"
#include "input/inputserver.h"
#include "input/keyboard.h"
#include "dynui/im3d/im3dcontext.h"
#include "imgui.h"
#include "util/random.h"
#include "characters/charactercontext.h"
#include "models/nodes/shaderstatenode.h"
#include "dynui/im3d/im3d.h"
#include "lighting/lightcontext.h"
#include "decals/decalcontext.h"
#include "resources/resourceserver.h"
#include "terrain/terraincontext.h"
#include "scripting/python/pythonserver.h"
#include "io/console.h"
#include "util/random.h"

#include "coregraphics/legacy/nvx2streamreader.h"
#include "coregraphics/gpubuffertypes.h"
#include "core/debug.h"
#include "math/vec2.h"

namespace Demo
{

__ImplementSingleton(NavMesh);
    
void NavMesh::Init() 
{
    Singleton = n_new(NavMesh);
}

void NavMesh::Load(const char* filename)
{
    Ptr<IO::Stream> stream = IO::IoServer::Instance()->CreateStream(IO::URI("msh:navigation/navmesh.nvx2"));
    Ptr<Legacy::Nvx2StreamReader> nvx2Reader = Legacy::Nvx2StreamReader::Create();
    nvx2Reader->SetStream(stream);
    nvx2Reader->SetUsage(CoreGraphics::GpuBufferTypes::UsageImmutable);
    nvx2Reader->SetAccess(CoreGraphics::GpuBufferTypes::AccessNone);
    nvx2Reader->SetRawMode(true);

    if(!nvx2Reader->Open(nullptr))
    {
        // handle error
        //n_assert(false, "Failed to open navmesh");
    }

    float* verticiesData = nvx2Reader->GetVertexData();
    int vertWidth = nvx2Reader->GetVertexWidth();

    n_printf("Vertex width: %d\n", nvx2Reader->GetVertexWidth());
    n_printf("Num vertices: %d\n", nvx2Reader->GetNumVertices());
    n_printf("Num indices: %d\n", nvx2Reader->GetNumIndices());
    n_printf("Num edges: %d\n", nvx2Reader->GetNumEdges());
    auto indices = nvx2Reader->GetIndexData();

    for (int i = 0; i < nvx2Reader->GetNumVertices(); i++) {
        verticies.Append(Math::vec3(verticiesData[i*vertWidth], verticiesData[i * vertWidth+1], verticiesData[i * vertWidth+2]));
    }

    for (int i = 0; i < nvx2Reader->GetNumIndices(); i += 3) {
        int indexA = nvx2Reader->GetIndexData()[i * 2];
        int indexB = nvx2Reader->GetIndexData()[i * 2 + 2];
        int indexC = nvx2Reader->GetIndexData()[i * 2 + 4];

        int faceIndex = (int)faces.size();
        int edgeIndex = (int)halfEdgeArray.size();
        halfEdgeArray.Append(HalfEdge{indexA, edgeIndex+1, -1, faceIndex});
        halfEdgeArray.Append(HalfEdge{indexB, edgeIndex+2, -1, faceIndex});
        halfEdgeArray.Append(HalfEdge{indexC, edgeIndex+0, -1, faceIndex});

        faces.Append(edgeIndex);

    }

    for (int i = 0; i < halfEdgeArray.size(); i++) {
        if (halfEdgeArray[i].neighbourEdge >= 0) // HalfEdge already has neighbour
            continue;
        for (int j = 0; j < halfEdgeArray.size(); j++) {
            if (i == j)
                continue;
            int l1p1 = halfEdgeArray[i].vertIdx;
            int l2p1 = halfEdgeArray[j].vertIdx;
            int l1p2 = halfEdgeArray[halfEdgeArray[i].nextEdge].vertIdx;
            int l2p2 = halfEdgeArray[halfEdgeArray[j].nextEdge].vertIdx;
            if ((l1p1 == l2p1 && l1p2 == l2p2) ||
                (l1p1 == l2p2 && l1p2 == l2p1)) {
                halfEdgeArray[i].neighbourEdge = j;
                halfEdgeArray[j].neighbourEdge = i;
                break;
            }
        }
    }
}

void NavMesh::recDraw(int edge, int recDepth) {
    if (recDepth <= 0)
        return;
    if (edge == -1)
        return;
    for (int j = 0; j < 3; j++) {
        int vertexA = halfEdgeArray[edge].vertIdx;
        edge = halfEdgeArray[edge].nextEdge;
        int vertexB = halfEdgeArray[edge].vertIdx;
        auto pA = verticies[vertexA] + Math::vec3(0, 2, 0);
        auto pB = verticies[vertexB] + Math::vec3(0, 2, 0);
        Im3d::Im3dContext::DrawLine(Math::line(pA, pB), 10, Math::vec4(0.7, 0, 1, 1));
        recDraw(halfEdgeArray[edge].neighbourEdge, recDepth-1);
    }
}

int NavMesh::getFace(int num)
{ 
    return Singleton->faces[num];
}
Math::vec3 NavMesh::getVertex(int num)
{
    return Singleton->verticies[num];
}
HalfEdge NavMesh::getHalfEdge(int num)
{
    return Singleton->halfEdgeArray[num];
}
int  NavMesh::getNumFace()
{
    return (int)Singleton->faces.size();
}
int NavMesh::getNumVertex()
{
    return (int)Singleton->verticies.size();
}
int NavMesh::getNumHalfEdge()
{
    return (int)Singleton->halfEdgeArray.size();
}
Math::vec3 NavMesh::getCenter(int face_idx)
{
    Math::vec3 pointA = Singleton->verticies[Singleton->halfEdgeArray[Singleton->faces[face_idx]].vertIdx];
    Math::vec3 pointB = Singleton->verticies[Singleton->halfEdgeArray[Singleton->faces[face_idx]+1].vertIdx];
    Math::vec3 pointC = Singleton->verticies[Singleton->halfEdgeArray[Singleton->faces[face_idx]+2].vertIdx];
    return (pointA + pointB + pointC) * .3333333433F;
}
Math::vec3 NavMesh::getCenterOfFace(int face)
{
    Math::vec3 pointA = Singleton->verticies[Singleton->halfEdgeArray[face].vertIdx];
    Math::vec3 pointB = Singleton->verticies[Singleton->halfEdgeArray[face+1].vertIdx];
    Math::vec3 pointC = Singleton->verticies[Singleton->halfEdgeArray[face+2].vertIdx];
    return (pointA + pointB + pointC) * .3333333433F;
}


//source:https://stackoverflow.com/questions/2049582/how-to-determine-if-a-point-is-in-a-2d-triangle

// a and b make up the line and p is the point to check
float sign(Math::vec2 p, Math::vec2 a, Math::vec2 b)
{
    return (p.x - b.x) * (a.y - b.y) - (a.x - b.x) * (p.y - b.y);
}

bool NavMesh::isInTriangle(Math::vec2 p, int face)
{
    Math::vec3 a3 = Singleton->verticies[Singleton->halfEdgeArray[Singleton->faces[face]].vertIdx];
    Math::vec3 b3 = Singleton->verticies[Singleton->halfEdgeArray[Singleton->faces[face] + 1].vertIdx];
    Math::vec3 c3 = Singleton->verticies[Singleton->halfEdgeArray[Singleton->faces[face] + 2].vertIdx];

    Math::vec2 a = Math::vec2(a3.x, a3.z);
    Math::vec2 b = Math::vec2(b3.x, b3.z);
    Math::vec2 c = Math::vec2(c3.x, c3.z);

    float d1, d2, d3;
    bool has_neg, has_pos;

    d1 = sign(p, a, b);
    d2 = sign(p, b, c);
    d3 = sign(p, c, a);

    has_neg = (d1 < 0) || (d2 < 0) || (d3 < 0);
    has_pos = (d1 > 0) || (d2 > 0) || (d3 > 0);

    return !(has_neg && has_pos);

}

bool NavMesh::isInFace(Math::vec2 p, int face)
{
    Math::vec3 a3 = Singleton->verticies[Singleton->halfEdgeArray[face].vertIdx];
    Math::vec3 b3 = Singleton->verticies[Singleton->halfEdgeArray[face + 1].vertIdx];
    Math::vec3 c3 = Singleton->verticies[Singleton->halfEdgeArray[face + 2].vertIdx];

    Math::vec2 a = Math::vec2(a3.x, a3.z);
    Math::vec2 b = Math::vec2(b3.x, b3.z);
    Math::vec2 c = Math::vec2(c3.x, c3.z);

    float d1, d2, d3;
    bool has_neg, has_pos;

    d1 = sign(p, a, b);
    d2 = sign(p, b, c);
    d3 = sign(p, c, a);

    has_neg = (d1 < 0) || (d2 < 0) || (d3 < 0);
    has_pos = (d1 > 0) || (d2 > 0) || (d3 > 0);

    return !(has_neg && has_pos);

}

//endsource

bool NavMesh::isOnNavMesh(Math::vec2 p)
{
    for (int i = 0; i < Singleton->getNumFace(); i++)
    {
        if (NavMesh::isInTriangle(p, i)) return true;
    }

    return false;
}

int NavMesh::findInNavMesh(Math::vec2 p)
{
    for (int i = 0; i < Singleton->getNumFace(); i++)
    {
        if (NavMesh::isInTriangle(p, i)) 
        {
            n_printf("Found face idx: %d", i);
            return Singleton->faces[i];
        }
    }

    return -1;
}

void NavMesh::DbgDraw()
{

    //recDraw(0, 15);

    Math::vec4 colors[3] = {Math::vec4(1,0,0,1), Math::vec4(0,1,0,1), Math::vec4(0,0,1,1)};


    for (int i = 0; i < faces.size(); i++) {
        auto center = getCenter(i);
        int edgeIndex = faces[i];
        for (int j = 0; j < 3; j++) {
            int vertexA = halfEdgeArray[edgeIndex].vertIdx;
            edgeIndex = halfEdgeArray[edgeIndex].nextEdge;
            int vertexB = halfEdgeArray[edgeIndex].vertIdx;
            auto pA = verticies[vertexA] + Math::vec3(0,2,0);
            auto pB = verticies[vertexB] + Math::vec3(0,2,0);
    
            auto diffA = pA - center;
            auto lenA = Math::length(diffA);
            diffA = Math::normalize(diffA) * lenA * 0.8f;
            pA = center + diffA;
            
            auto diffB = pB - center;
            auto lenB = Math::length(diffB);
            diffB = Math::normalize(diffB) * lenB * 0.8f;
            pB = center + diffB;

            Im3d::Im3dContext::DrawLine(Math::line(pA, pB), 10, colors[j]);

        }
        Math::vec3 vector = getCenter(i);
        Im3d::Im3dContext::DrawPoint(Math::vec3(vector), 10, Math::vec4(0, 0, 0, 1));
    }
    

    /*for (int i = 0; i < nvx2Reader->GetNumIndices(); i += 3) {
        int indexA = vertWidth * nvx2Reader->GetIndexData()[i*2];
        int indexB = vertWidth * nvx2Reader->GetIndexData()[i*2+2];
        int indexC = vertWidth * nvx2Reader->GetIndexData()[i*2+4];



        Math::point pointA(verticies[indexA + 0], verticies[indexA + 1]+2, verticies[indexA + 2]);
        Math::point pointB(verticies[indexB + 0], verticies[indexB + 1]+2, verticies[indexB + 2]);
        Math::point pointC(verticies[indexC + 0], verticies[indexC + 1]+2, verticies[indexC + 2]);
        Im3d::Im3dContext::DrawLine(Math::line(pointA, pointB), 10, Math::vec4(0.7, 0, 1, 1));
        Im3d::Im3dContext::DrawLine(Math::line(pointB, pointC), 10, Math::vec4(0.7, 0, 1, 1));
        Im3d::Im3dContext::DrawLine(Math::line(pointC, pointA), 10, Math::vec4(0.7, 0, 1, 1));
    }*/
};

} // End namespace Demo
