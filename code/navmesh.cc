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
    n_printf("here\n");
    Ptr<IO::Stream> stream = IO::IoServer::Instance()->CreateStream(IO::URI("msh:navigation/navmesh.nvx2"));
    Ptr<Legacy::Nvx2StreamReader> nr = Legacy::Nvx2StreamReader::Create();
    this->nvx2Reader = nr;
    this->nvx2Reader->SetStream(stream);
    this->nvx2Reader->SetUsage(CoreGraphics::GpuBufferTypes::UsageImmutable);
    this->nvx2Reader->SetAccess(CoreGraphics::GpuBufferTypes::AccessNone);
    this->nvx2Reader->SetRawMode(true);

    if(this->nvx2Reader->IsRawMode())
        n_printf("RAW\n");

    n_printf("here\n");

    if(!this->nvx2Reader->Open(nullptr))
    {
        // handle error
        n_assert(false, "Failed to open navmesh");
    }

    n_printf("Vertex width: %d\n", this->nvx2Reader->GetVertexWidth());
    n_printf("Num vertices: %d\n", this->nvx2Reader->GetNumVertices());
    n_printf("Num indices: %d\n",  this->nvx2Reader->GetNumIndices());
}

void NavMesh::DbgDraw()
{
    
};

} // End namespace Demo
