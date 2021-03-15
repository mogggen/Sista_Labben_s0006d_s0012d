#ifndef NAVMESH_H
#define NAVMESH_H 

#include "core/refcounted.h"
#include "core/singleton.h"
#include "coregraphics/legacy/nvx2streamreader.h"

namespace Demo
{

class NavMesh
{
    __DeclareSingleton(NavMesh);
public:

    static void Init();
    void Load(const char* filename);
    void DbgDraw();
     
private:
    Ptr<Legacy::Nvx2StreamReader> nvx2Reader;
};

} // End namespace Demo


#endif /* NAVMESH_H */
