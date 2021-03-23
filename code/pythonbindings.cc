//------------------------------------------------------------------------------
//  pythonbindings.cc
//  (c) 2020 Magnus Lind
//------------------------------------------------------------------------------
#include "foundation/stdneb.h"
#include "pythonbindings.h"
#include "pybind11/pybind11.h"
#include "pybind11/operators.h"
#include "pybind11/functional.h"
#include "pybind11/cast.h"
#include "pybind11/pytypes.h"
#include "io/console.h"
#include "basegamefeature/managers/entitymanager.h"
#include "basegamefeature/managers/timemanager.h"
#include "game/api.h"
#include "math/mat4.h"
#include "math/point.h"
#include "timing/timer.h"
#include "properties/input.h"
#include "properties/movement.h"
#include "properties/agent.h"
#include "properties/health.h"
#include "properties/team.h"
#include "properties/building.h"
#include "properties/tree.h"
#include "properties/iron.h"
#include "imgui.h"
#include "dynui/im3d/im3dcontext.h"
#include "input/keyboard.h"
#include "managers/playermanager.h"
#include "graphicsfeature/graphicsfeatureunit.h"
#include "graphics/graphicsentity.h"
#include "models/modelcontext.h"
#include "ids/idgenerationpool.h"
#include "navmesh.h"

#define defPropertyAccessor(type, name) def_property(#name,\
        [](Game::Entity& e){\
            if(Game::HasProperty(e, Game::GetPropertyId(#name))) {\
                return py::cast(Game::GetProperty<type>(e, Game::GetPropertyId(#name)));\
            } else {\
                throw pybind11::value_error("This entity does not have a '" #name "' property.");\
            }\
        }, [](Game::Entity& e, pybind11::object obj) {\
            if(Game::HasProperty(e, Game::GetPropertyId(#name))) {\
                Game::SetProperty<type>(e, Game::GetPropertyId(#name), pybind11::cast<type>(obj));\
            } else {\
                throw pybind11::value_error("This entity does not have a '" #name "' property.");\
            }\
        })

#define defReadWrite(s, field) def_readwrite(#field, &s::field)
#define defReadWriteVec3(s, field) def_property(#field,\
        [](s& e){ return pybind11::cast(Math::point(e.field));},\
        [](s& e, pybind11::object obj){ e.field = pybind11::cast<Math::point>(obj).vec;})

namespace Python
{

namespace py = pybind11;

PYBIND11_EMBEDDED_MODULE(demo, m)
{
    py::class_<Game::Entity>(m, "Entity")
        .defPropertyAccessor(Math::mat4,              WorldTransform)
        .defPropertyAccessor(Demo::PlayerInput,       PlayerInput)
        .defPropertyAccessor(Demo::TopdownCamera,     TopdownCamera)
        .defPropertyAccessor(Demo::Movement,          Movement)
        .defPropertyAccessor(Demo::Marker,            Marker)
        .defPropertyAccessor(Demo::Agent,             Agent)
        .defPropertyAccessor(Demo::Health,            Health)
        .defPropertyAccessor(Demo::Team,              Team)
        .defPropertyAccessor(Demo::Building,          Building)
        .defPropertyAccessor(Demo::Tree,              Tree)
        .defPropertyAccessor(Demo::Iron,              Iron)
        .defPropertyAccessor(GraphicsFeature::Camera, Camera)
        .def(py::self == py::self);

    m.def("Delete", [](Game::Entity& e)
            {
                Game::DeleteEntity(e);
            });

    m.def("IsValid", [](Game::Entity& e)
            {
                return Game::IsValid(e);
            });

    py::class_<Demo::PlayerInput>(m, "PlayerInput")
        .defReadWrite(Demo::PlayerInput, forward)
        .defReadWrite(Demo::PlayerInput, strafe)
        .defReadWrite(Demo::PlayerInput, left_mouse)
        .defReadWrite(Demo::PlayerInput, right_mouse);

    py::class_<GraphicsFeature::Camera>(m, "Camera")
        .defReadWrite(GraphicsFeature::Camera, viewHandle)
        .defReadWrite(GraphicsFeature::Camera, localTransform)
        .defReadWrite(GraphicsFeature::Camera, fieldOfView)
        .defReadWrite(GraphicsFeature::Camera, aspectRatio)
        .defReadWrite(GraphicsFeature::Camera, zNear)
        .defReadWrite(GraphicsFeature::Camera, zFar)
        .defReadWrite(GraphicsFeature::Camera, orthographicWidth);
    
    py::class_<Demo::TopdownCamera>(m, "TopdownCamera")
        .defReadWrite(Demo::TopdownCamera, height)
        .defReadWrite(Demo::TopdownCamera, pitch)
        .defReadWrite(Demo::TopdownCamera, yaw);
    
    py::class_<Demo::Movement>(m, "Movement")
        .defReadWriteVec3(Demo::Movement, direction)
        .defReadWrite(Demo::Movement, speed)
        .defReadWrite(Demo::Movement, wanderRadius)
        .defReadWrite(Demo::Movement, wanderDistance)
        .defReadWrite(Demo::Movement, wanderJitter)
        .defReadWrite(Demo::Movement, maximumDistance)
        .defReadWrite(Demo::Movement, target_entity);
    
    py::class_<Demo::Marker>(m, "Marker")
        .defReadWriteVec3(Demo::Marker, position);
 
    py::class_<Demo::Agent>(m, "Agent")
        .defReadWriteVec3(Demo::Agent, position)
        .defReadWriteVec3(Demo::Agent, targetPosition)
        .defReadWrite(Demo::Agent, type);

    py::class_<Demo::Tree>(m, "Tree")
        .defReadWriteVec3(Demo::Tree, position);

    py::class_<Demo::Iron>(m, "Iron")
        .defReadWriteVec3(Demo::Iron, position);

    py::enum_<Demo::agentType>(m, "agentType")
        .value("WORKER", Demo::WORKER)
        .value("SCOUT", Demo::SCOUT)
        .value("SOLDIER", Demo::SOLDIER)
        .value("KILNER", Demo::KILNER)
        .value("SMITH", Demo::SMITH)
        .value("SMELTER", Demo::SMELTER)
        .value("BUILDER", Demo::BUILDER)
        .export_values();

    py::class_<Demo::Building>(m, "Building")
        .defReadWriteVec3(Demo::Building, position)
        .defReadWrite(Demo::Building, hasWorker)
        .defReadWrite(Demo::Building, type);

    py::enum_<Demo::buildingType>(m, "buildingType")
        .value("KILN", Demo::KILN)
        .value("SMELTERY", Demo::SMELTERY)
        .value("BLACKSMITH", Demo::BLACKSMITH)
        .value("TRAININGCAMP", Demo::TRAININGCAMP)
        .value("CASTLE", Demo::CASTLE)
        .export_values();

    py::class_<Demo::Health>(m, "Health")
        .defReadWrite(Demo::Health, hp);

    py::class_<Demo::Team>(m, "Team")
        .defReadWrite(Demo::Team, team);

    py::enum_<Demo::teamEnum>(m, "teamEnum")
        .value("GRUPP_1", Demo::GRUPP_1)
        .value("GRUPP_2", Demo::GRUPP_2)
        .export_values();

    m.def("ForHealthTeam",[](std::function<void(Demo::Health&, Demo::Team&)> &callback)
    {
        Game::FilterCreateInfo info;
        info.inclusive[0] = Game::GetPropertyId("Health");
        info.access[0]    = Game::AccessMode::READ;
        info.inclusive[1] = Game::GetPropertyId("Team");
        info.access[1]    = Game::AccessMode::READ;
        info.numInclusive = 2;

        Game::Filter ht_filter = Game::CreateFilter(info);

        Game::Dataset ht_data = Game::Query(ht_filter);
        for (int v = 0; v < ht_data.numViews; v++)
        {
            Game::Dataset::CategoryTableView const& view = ht_data.views[v];
            Demo::Health* const healths = (Demo::Health*)view.buffers[0];
            Demo::Team* const teams = (Demo::Team*)view.buffers[1];

            for (IndexT i = 0; i < view.numInstances; ++i)
            {
                callback(healths[i], teams[i]);
            }
        }
    });
    m.def("ForAgentTeam",[](std::function<void(Demo::Agent&, Demo::Team&)> &callback)
    {
        Game::FilterCreateInfo info;
        info.inclusive[0] = Game::GetPropertyId("Agent");
        info.access[0]    = Game::AccessMode::READ;
        info.inclusive[1] = Game::GetPropertyId("Team");
        info.access[1]    = Game::AccessMode::READ;
        info.numInclusive = 2;

        Game::Filter filter = Game::CreateFilter(info);

        Game::Dataset data = Game::Query(filter);
        for (int v = 0; v < data.numViews; v++)
        {
            Game::Dataset::CategoryTableView const& view = data.views[v];
            Demo::Agent* const agents = (Demo::Agent*)view.buffers[0];
            Demo::Team* const teams = (Demo::Team*)view.buffers[1];

            for (IndexT i = 0; i < view.numInstances; ++i)
            {
                callback(agents[i], teams[i]);
            }
        }
    });
    m.def("ForBuildingTeam",[](std::function<void(Demo::Building&, Demo::Team&)> &callback)
    {
        Game::FilterCreateInfo info;
        info.inclusive[0] = Game::GetPropertyId("Building");
        info.access[0]    = Game::AccessMode::READ;
        info.inclusive[1] = Game::GetPropertyId("Team");
        info.access[1]    = Game::AccessMode::READ;
        info.numInclusive = 2;

        Game::Filter filter = Game::CreateFilter(info);

        Game::Dataset data = Game::Query(filter);
        for (int v = 0; v < data.numViews; v++)
        {
            Game::Dataset::CategoryTableView const& view = data.views[v];
            Demo::Building* const buildings = (Demo::Building*)view.buffers[0];
            Demo::Team* const teams = (Demo::Team*)view.buffers[1];

            for (IndexT i = 0; i < view.numInstances; ++i)
            {
                callback(buildings[i], teams[i]);
            }
        }
    });
    m.def("ForAgentHealthTeam",[](std::function<void(Demo::Agent&, Demo::Health&, Demo::Team&)> &callback)
    {
        Game::FilterCreateInfo info;
        info.inclusive[0] = Game::GetPropertyId("Agent");
        info.access[0]    = Game::AccessMode::READ;
        info.inclusive[1] = Game::GetPropertyId("Health");
        info.access[1]    = Game::AccessMode::READ;
        info.inclusive[2] = Game::GetPropertyId("Team");
        info.access[2]    = Game::AccessMode::READ;
        info.numInclusive = 3;

        Game::Filter filter = Game::CreateFilter(info);

        Game::Dataset data = Game::Query(filter);
        for (int v = 0; v < data.numViews; v++)
        {
            Game::Dataset::CategoryTableView const& view = data.views[v];
            Demo::Agent* const agents = (Demo::Agent*)view.buffers[0];
            Demo::Health* const healths = (Demo::Health*)view.buffers[1];
            Demo::Team* const teams = (Demo::Team*)view.buffers[2];

            for (IndexT i = 0; i < view.numInstances; ++i)
            {
                callback(agents[i], healths[i], teams[i]);
            }
        }
    });
    m.def("ForBuildingHealthTeam",[](std::function<void(Demo::Building&, Demo::Health&, Demo::Team&)> &callback)
    {
        Game::FilterCreateInfo info;
        info.inclusive[0] = Game::GetPropertyId("Building");
        info.access[0]    = Game::AccessMode::READ;
        info.inclusive[1] = Game::GetPropertyId("Health");
        info.access[1]    = Game::AccessMode::READ;
        info.inclusive[2] = Game::GetPropertyId("Team");
        info.access[2]    = Game::AccessMode::READ;
        info.numInclusive = 3;

        Game::Filter filter = Game::CreateFilter(info);

        Game::Dataset data = Game::Query(filter);
        for (int v = 0; v < data.numViews; v++)
        {
            Game::Dataset::CategoryTableView const& view = data.views[v];
            Demo::Building* const buildings = (Demo::Building*)view.buffers[0];
            Demo::Health* const healths = (Demo::Health*)view.buffers[1];
            Demo::Team* const teams = (Demo::Team*)view.buffers[2];

            for (IndexT i = 0; i < view.numInstances; ++i)
            {
                callback(buildings[i], healths[i], teams[i]);
            }
        }
    });

    m.def("HelloSayer", [](){IO::Console::Instance()->Print("I am saying HELLO!!!");}, "Says hello.");
    m.def("SpawnCube", [](Math::point& p){
            Game::EntityCreateInfo info;
            info.immediate = true;
            info.templateId = Game::GetTemplateId("MovingEntity/cube"_atm);
            Game::Entity entity = Game::CreateEntity(info);
            Game::SetProperty(entity, Game::GetPropertyId("WorldTransform"_atm), Math::translation(p.vec));
            return entity;
            });

    m.def("SpawnEntity", [](char* name){
            Util::StringAtom atom = Util::StringAtom(name);
            Game::EntityCreateInfo info;
            info.immediate = true;
            info.templateId = Game::GetTemplateId(atom);
            auto e = Game::CreateEntity(info);
            //n_printf("created entity %d %d\n", Ids::Generation(e.id), Ids::Index(e.id));
            return e;
            });

    m.def("GetPlayer", [](){return Demo::PlayerManager::Instance()->get_player();});
    m.def("SetCameraPos", [](Math::point p){Demo::PlayerManager::Instance()->set_target_pos(p);});


    m.def("GetTime",       [](){return Game::TimeManager::GetTimeSource(TIMESOURCE_GAMEPLAY)->time;});
    m.def("GetFrameTime",  [](){return Game::TimeManager::GetTimeSource(TIMESOURCE_GAMEPLAY)->frameTime;});
    m.def("PauseTime",     [](){Game::TimeManager::GetTimeSource(TIMESOURCE_GAMEPLAY)->pauseCounter++;});
    m.def("UnPauseTime",   [](){Game::TimeManager::GetTimeSource(TIMESOURCE_GAMEPLAY)->pauseCounter--;});
    m.def("SetTimeFactor", [](float factor){Game::TimeManager::GetTimeSource(TIMESOURCE_GAMEPLAY)->timeFactor = factor;});

    m.def("IsLeftMouseDown", []() -> bool
            {
                 auto input = Game::GetProperty<Demo::PlayerInput>(Demo::PlayerManager::Instance()->get_player(), Game::GetPropertyId("PlayerInput"_atm));
                 return input.left_mouse;
            });
    m.def("IsRightMouseDown", []() -> bool
            {
                 auto input = Game::GetProperty<Demo::PlayerInput>(Demo::PlayerManager::Instance()->get_player(), Game::GetPropertyId("PlayerInput"_atm));
                 return input.right_mouse;
            });
    m.def("RayCastMousePos", []()
            {
                auto p = Demo::PlayerManager::RayCastMousePos();
                return Math::point(p.vec);
            });

    m.def("IsTabDown", []()
            {
                auto& io = ImGui::GetIO();
                if (!io.WantCaptureMouse)
                    return io.KeysDown[Input::Key::Tab];
                else
                    return false;
            });
    m.def("IsPdown", []()
            {
                auto& io = ImGui::GetIO();
                if (!io.WantCaptureMouse)
                    return io.KeysDown[Input::Key::P];
                else
                    return false;
            });
    m.def("IsUpdown", []()
            {
                auto& io = ImGui::GetIO();
                if (!io.WantCaptureMouse)
                    return io.KeysDown[Input::Key::Up];
                else
                    return false;
            });
    m.def("IsDowndown", []()
            {
                auto& io = ImGui::GetIO();
                if (!io.WantCaptureMouse)
                    return io.KeysDown[Input::Key::Down];
                else
                    return false;
            });
    m.def("IsYDown", []()
            {
                auto& io = ImGui::GetIO();
                if (!io.WantCaptureMouse)
                    return io.KeysDown[Input::Key::Y];
                else
                    return false;
            });

    m.def("DrawDot", [](Math::point& p, float size, Math::vec4& color)
            {
                Math::vec3 v = p.vec;
                Im3d::Im3dContext::DrawPoint(v, size, color);
            });
    m.def("DrawLine", [](Math::point& p1, Math::point& p2, float size, Math::vec4& color)
            {
                Im3d::Im3dContext::DrawLine(Math::line(p1,p2), size, color);
            });
    m.def("DrawBox", [](Math::point& p, float size, Math::vec4& color)
            {
                Math::mat4 m = Math::scaling(size) * Math::translation(p.vec);
                Im3d::Im3dContext::DrawBox(m, color);
            });
}



PYBIND11_EMBEDDED_MODULE(imgui, m)
{
    m.def("Begin", &ImGui::Begin);
    m.def("End", &ImGui::End);
    m.def("Text", [](const char* text){ImGui::TextUnformatted(text);});
}

PYBIND11_EMBEDDED_MODULE(navMesh, m)
{
    py::class_<Demo::HalfEdge>(m, "HalfEdge")
        .def_readwrite("vertIdx", &Demo::HalfEdge::vertIdx)
        .def_readwrite("nextEdge", &Demo::HalfEdge::nextEdge)
        .def_readwrite("neighbourEdge", &Demo::HalfEdge::neighbourEdge)
        .def_readwrite("face", &Demo::HalfEdge::face);


    m.def("getVertex", [](int num)
        {
            auto vertex = Demo::NavMesh::getVertex(num);
            return Math::point(vertex);
        });
    m.def("getHalfEdge", &Demo::NavMesh::getHalfEdge);
    m.def("getFace", &Demo::NavMesh::getFace);
    m.def("getNumVertex", &Demo::NavMesh::getNumVertex);
    m.def("getNumHalfEdge", &Demo::NavMesh::getNumHalfEdge);
    m.def("getNumFace", &Demo::NavMesh::getNumFace);
    m.def("getCenter", [](int num)
        {
            auto vertex = Demo::NavMesh::getCenter(num);
            return Math::point(vertex);
        });
    m.def("getCenterOfFace", [](int num)
        {
            auto vertex = Demo::NavMesh::getCenterOfFace(num);
            return Math::point(vertex);
        });
    m.def("isInTriangle", &Demo::NavMesh::isInTriangle);
    m.def("isInFace", &Demo::NavMesh::isInFace);
    m.def("isOnNavMesh", &Demo::NavMesh::isOnNavMesh);
    m.def("findInNavMesh", &Demo::NavMesh::findInNavMesh);
}
}
