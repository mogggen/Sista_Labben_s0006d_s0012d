//------------------------------------------------------------------------------
//  gamestatemanager.cc
//  (C) 2020 Individual contributors, see AUTHORS file
//------------------------------------------------------------------------------
#include "application/stdneb.h"
#include "gamestatemanager.h"
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

#include "navmesh.h"

#include <chrono>

#ifdef __WIN32__
#include <shellapi.h>
#elif __LINUX__

#endif

namespace Demo
{

__ImplementSingleton(GameStateManager)

//------------------------------------------------------------------------------
/**
*/
Game::ManagerAPI
GameStateManager::Create()
{
    n_assert(!GameStateManager::HasInstance());
    Singleton = n_new(GameStateManager);

    Game::ManagerAPI api;
    api.OnActivate = &GameStateManager::OnActivate;
    api.OnBeginFrame = &GameStateManager::OnBeginFrame;
    api.OnFrame = &GameStateManager::OnFrame;
    return api;
}

//------------------------------------------------------------------------------
/**
*/
void
GameStateManager::Destroy()
{
    n_assert(GameStateManager::HasInstance());
    n_delete(Singleton);
}

//------------------------------------------------------------------------------
/**
*/
GameStateManager::GameStateManager()
{
    // empty
}

//------------------------------------------------------------------------------
/**
*/
GameStateManager::~GameStateManager()
{
    // empty
}

//------------------------------------------------------------------------------
/**
*/
void
GameStateManager::OnActivate()
{
    { // ## Temp: Preload all resources ##
        auto Preload = [](Resources::ResourceName const& modelName)
        {
            auto entity = Graphics::CreateEntity();
            Graphics::RegisterEntity<Models::ModelContext>(entity);
            Models::ModelContext::Setup(entity, modelName, "TemporaryPreload", [entity]()
            {});
        };

        Preload("mdl:dev/ground.n3");
        Preload("mdl:dev/knob_metallic.n3");
        Preload("mdl:dev/knob_plastic_scuffed.n3");
        Preload("mdl:dev/knob_reflective.n3");
        Preload("mdl:dev/scene.n3");
        Preload("mdl:dev/tree.n3");
        Preload("mdl:dev/mountain.n3");
        Preload("mdl:dev/water.n3");
        Preload("mdl:dev/ground.n3");
        Preload("mdl:dev/quagmire.n3");
        Preload("mdl:dev/guy.n3");
        Preload("mdl:dev/cloud.n3");
        Preload("mdl:team_units/red_Unit_Footman.n3");
        
    } // #################################

    //
    // Copy 'n' pasted from nota.cc
    //
    {
        auto gid = Graphics::CreateEntity();Graphics::RegisterEntity<Models::ModelContext, Visibility::ObservableContext>(gid);
        Models::ModelContext::Setup(gid, "mdl:environment/Groundplane.n3", "gid", [gid]()
                {
                    Visibility::ObservableContext::Setup(gid, Visibility::VisibilityEntityType::Model);
                    Models::ModelContext::SetTransform(gid, Math::translation(Math::vec3(0,0, 0)));
                });
    }
    Util::String models[] = {
        "mdl:Vegetation/Ferns_01.n3",
        "mdl:Vegetation/Ferns_02.n3",
        "mdl:Vegetation/Ferns_03.n3",
        "mdl:Vegetation/Ferns_04.n3",
        "mdl:Vegetation/Ferns_05.n3",
        "mdl:Vegetation/Ferns_06.n3",
        "mdl:Vegetation/Ferns_07.n3",
        "mdl:Vegetation/Ferns_08.n3",
        "mdl:Vegetation/Ferns_09.n3",
        "mdl:Vegetation/Ferns_10.n3",
        "mdl:Vegetation/Ferns_11.n3",
        "mdl:Vegetation/Ferns_12.n3",
        "mdl:Vegetation/Ferns_13.n3",
        "mdl:Vegetation/Ferns_14.n3",
        "mdl:Vegetation/Trees_01.n3",
        "mdl:Vegetation/Trees_02.n3",
        "mdl:Vegetation/Trees_03.n3",
        "mdl:Vegetation/Trees_04.n3",
        "mdl:Vegetation/Trees_05.n3",
        "mdl:Vegetation/Trees_06.n3",
        "mdl:Vegetation/Trees_07.n3",
        "mdl:Vegetation/Trees_08.n3",
        "mdl:Vegetation/Trees_09.n3",
        "mdl:Vegetation/Trees_10.n3",
        "mdl:Vegetation/Trees_11.n3",
        "mdl:Vegetation/Trees_12.n3",
        "mdl:Vegetation/Trees_13.n3",
        "mdl:environment/Bridge.n3",
        "mdl:environment/env_prop_1.n3",
        "mdl:environment/env_prop_2.n3",
    };

    for (auto& model : models)
    {
        auto gid = Graphics::CreateEntity();
        Graphics::RegisterEntity<Models::ModelContext, Visibility::ObservableContext>(gid);
        Models::ModelContext::Setup(gid, model, "gid", [gid]()
            {
                Visibility::ObservableContext::Setup(gid, Visibility::VisibilityEntityType::Model);
                Models::ModelContext::SetTransform(gid, Math::translation(Math::vec3(0,0, 0)));
            });

    }
    
    // Generate mountains
    Util::String mountainRes = "mdl:environment/Mountains_01.n3";
    float width = 395 * 1.1f;
    float height = 420 * 1.1f;
    int nw = 8;
    int nh = 8;
    for (int y = 0; y <= nh; y++)
    {
        for (int x = 0; x <= nw; x++)
        {
            if (x == 0 || y == 0 || x == nw || y == nh)
            {
                Math::vec3 pos = Math::vec3((width / nw) * (float)x - (width / 2.0f), 0, (height / nh) * (float)y - (height / 2.0f) - 20.0f);
                auto gid = Graphics::CreateEntity();
                Graphics::RegisterEntity<Models::ModelContext, Visibility::ObservableContext>(gid);
                Models::ModelContext::Setup(gid, mountainRes, "gid", [gid, pos]()
                    {
                        Visibility::ObservableContext::Setup(gid, Visibility::VisibilityEntityType::Model);
                        float scale = Util::RandomFloat() * 0.4f + 1.0f;
                        Models::ModelContext::SetTransform(gid, Math::scaling(scale) * Math::rotationy(Util::RandomFloat()) * Math::translation(pos));
                    });
            }
        }
    }

    const Util::StringAtom modelRes[] = { "mdl:team_units/blue_Unit_Archer.n3",  "mdl:team_units/blue_Unit_Footman.n3",  "mdl:team_units/blue_Unit_Spearman.n3" };
    const Util::StringAtom skeletonRes[] = { "ske:Units/Unit_Archer.nsk3",  "ske:Units/Unit_Footman.nsk3",  "ske:Units/Unit_Spearman.nsk3" };
    const Util::StringAtom animationRes[] = { "ani:Units/Unit_Archer.nax3",  "ani:Units/Unit_Footman.nax3",  "ani:Units/Unit_Spearman.nax3" };
    
//for (int i = 0; i < 3; i++){auto gid = Graphics::CreateEntity();Graphics::RegisterEntity<Models::ModelContext, Visibility::ObservableContext,Characters::CharacterContext>(gid);Models::ModelContext::Setup(gid, modelRes[i], "gid", [gid, i](){Visibility::ObservableContext::Setup(gid, Visibility::VisibilityEntityType::Model);Models::ModelContext::SetTransform(gid, Math::translation(Math::vec3(0,0, i * 2)));});Characters::CharacterContext::Setup(gid, skeletonRes[i], animationRes[i], "Viewer");Characters::CharacterContext::PlayClip(gid, nullptr, 0, 0, Characters::Append, 1.0f, 1, Util::RandomFloat() * 100.0f, 0.0f, 0.0f, Util::RandomFloat() * 100.0f);}



    //
    // end copy 'n' paste
    //

    //
    // Loading in navmesh
    //
   
    NavMesh::Init();
    NavMesh::Instance()->Load("msh:navigation/navmesh.nvx2");

    GraphicsFeature::GraphicsFeatureUnit::Instance()->AddRenderUICallback([]()
    {
        //NavMesh::Instance()->DbgDraw();
        Scripting::ScriptServer::Instance()->Eval("NebulaDraw()");
    });

    //GraphicsFeature::GraphicsFeatureUnit::Instance()->SetGraphicsDebugging(true);
}

//------------------------------------------------------------------------------
/**
*/
void
GameStateManager::OnBeginFrame()
{
    if (Input::InputServer::Instance()->GetDefaultKeyboard()->KeyPressed(Input::Key::Escape))
    {
        Core::SysFunc::Exit(0);
    }
    
    Scripting::ScriptServer::Instance()->Eval("NebulaUpdate()");
}

//------------------------------------------------------------------------------
/**
*/
void
GameStateManager::OnFrame()
{
#if __NEBULA_HTTP__
    if (Input::InputServer::Instance()->GetDefaultKeyboard()->KeyDown(Input::Key::F1))
    {
        // Open browser with debug page.
        Util::String url = "http://localhost:2100";
#ifdef __WIN32__
        ShellExecute(0, 0, url.AsCharPtr(), 0, 0, SW_SHOW);
#elif __LINUX__
        Util::String shellCommand = "open ";
        shellCommand.Append(url);
        system(shellCommand.AsCharPtr());
#else
        n_printf("Cannot open browser. URL is %s\n", url.AsCharPtr());
#endif
    }
#endif
}

} // namespace Game
