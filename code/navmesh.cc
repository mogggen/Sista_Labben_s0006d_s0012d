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
        n_assert(false, "Failed to open navmesh");
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

        int faceIndex = faces.size();
        int edgeIndex = halfEdgeArray.size();
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

void NavMesh::DbgDraw()
{

    //recDraw(0, 15);



   /* for (int i = 0; i < faces.size(); i++) {
        int edgeIndex = faces[i];
        for (int j = 0; j < 3; j++) {
            int vertexA = halfEdgeArray[edgeIndex].vertIdx;
            edgeIndex = halfEdgeArray[edgeIndex].nextEdge;
            int vertexB = halfEdgeArray[edgeIndex].vertIdx;
            auto pA = verticies[vertexA] + Math::vec3(0,2,0);
            auto pB = verticies[vertexB] + Math::vec3(0,2,0);
            Im3d::Im3dContext::DrawLine(Math::line(pA, pB), 10, Math::vec4(0.7, 0, 1, 1));

        }
    }*/

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
