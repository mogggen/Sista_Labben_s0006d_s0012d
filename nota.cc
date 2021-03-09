{
	auto gid = Graphics::CreateEntity();
	Graphics::RegisterEntity<Models::ModelContext, Visibility::ObservableContext>(gid);
	Models::ModelContext::Setup(gid, "mdl:environment/Groundplane.n3", "gid", [gid]()
	{
		Visibility::ObservableContext::Setup(gid, Visibility::VisibilityEntityType::Model);
		Models::ModelContext::SetTransform(gid, Math::translation(Math::vec3(0, 0, 0)));
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
		Models::ModelContext::SetTransform(gid, Math::translation(Math::vec3(0, 0, 0)));
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

for (int i = 0; i < 3; i++)
{
	auto gid = Graphics::CreateEntity();
	Graphics::RegisterEntity<Models::ModelContext, Visibility::ObservableContext, Characters::CharacterContext>(gid);
	Models::ModelContext::Setup(gid, modelRes[i], "gid", [gid, i]()
	{
		Visibility::ObservableContext::Setup(gid, Visibility::VisibilityEntityType::Model);
		Models::ModelContext::SetTransform(gid, Math::translation(Math::vec3(0, 0, i * 2)));
	});
	Characters::CharacterContext::Setup(gid, skeletonRes[i], animationRes[i], "Viewer");
	Characters::CharacterContext::PlayClip(gid, nullptr, 0, 0, Characters::Append, 1.0f, 1, Math::n_rand() * 100.0f, 0.0f, 0.0f, Math::n_rand() * 100.0f);
}

#######################################################

namespace Tools
{

class VertexTool
{
public:
    VertexTool();
    ~VertexTool();

    void Update();

    void SetGraphicsEntity(Graphics::GraphicsEntityId entity);
    void SetCameraEntity(Graphics::GraphicsEntityId cam);

private:
    Graphics::GraphicsEntityId entity;
    Graphics::GraphicsEntityId cam;
    IndexT hoveredIndex = 0;
    Util::Array<IndexT> selectedIndex = { 0 };

    Math::vec2 selectionStart;
    Math::vec2 selectionEnd;

    Util::Array<Graphics::GraphicsEntityId> brushes;

    //--------
    void* vbo;
    void* ibo;
    CoreGraphics::BufferId vb;
    CoreGraphics::BufferId ib;

    IndexT baseIndex;
    IndexT baseVertex;
    SizeT numIndices;
    SizeT numVertices;
    ubyte positionOffset;
    SizeT vertexSize;

    bool mapped = false;

    //----------
    Timing::Timer timer;
};

inline VertexTool::VertexTool()
{
    timer.Start();
}

inline VertexTool::~VertexTool()
{
    timer.Stop();
}

inline void VertexTool::Update()
{
    Ptr<Input::InputServer> inputServer = Input::InputServer::Instance();
    const Ptr<Input::Keyboard>& keyboard = inputServer->GetDefaultKeyboard();
    const Ptr<Input::Mouse>& mouse = inputServer->GetDefaultMouse();

    Timing::Time start = timer.GetTime();
    if (this->mapped)
    {
        Math::line line;
        line = RenderUtil::MouseRayUtil::ComputeWorldMouseRay(
            mouse->GetScreenPosition(),
            9999999.0f,
            Math::inverse(Graphics::CameraContext::GetTransform(this->cam)),
            Math::inverse(Graphics::CameraContext::GetProjection(this->cam)),
            Graphics::CameraContext::GetSettings(this->cam).GetZNear());

        float closestDistance = 999999999999.0f;

        const Util::Array<Models::ModelNode::Instance*>& nodes = Models::ModelContext::GetModelNodeInstances(this->entity);
        const auto& nodeTypes = Models::ModelContext::GetModelNodeTypes(this->entity);

        for (IndexT j = 0; j < numVertices; j++)
        {
            IndexT index = baseVertex + positionOffset + (j * vertexSize);
            float* v = (float*)&(((ubyte*)vbo)[index]);
            Math::point vertex(v[0], v[1], v[2]);

            float dist = line.distance(vertex);
            if (dist < closestDistance)
            {
                closestDistance = dist;
                hoveredIndex = index;
            }

            const Im3d::Color color = Im3d::Color(1.0, 1.0, 1.0, 1.0f);
            float size = 7.5f;

            Im3d::DrawPoint(Im3d::Vec3(vertex.x, vertex.y, vertex.z), size, color);
        }

        // Draw hovered index last
        Im3d::Color color = Im3d::Color(0.0, 0.8f, 0.0f, 1.0f);
        float size = 10.0f;
        float* vertex;
        vertex = ((float*)&(((ubyte*)vbo)[hoveredIndex]));
        Im3d::DrawPoint(Im3d::Vec3(vertex[0], vertex[1], vertex[2]), size, color);

        color = Im3d::Color_Red;
        size = 15.0f;
        vertex = ((float*)&(((ubyte*)vbo)[selectedIndex[0]]));
        Im3d::DrawPoint(Im3d::Vec3(vertex[0], vertex[1], vertex[2]), size, color);

        if (!keyboard->KeyPressed(Input::Key::Code::LeftMenu))
        {
            if (Im3d::GizmoTranslation("vertex", vertex, false))
            {
                // Nothing atm.
            }
            else
            {
                if (mouse->ButtonPressed(Input::MouseButton::Code::RightButton))
                {
                    this->selectedIndex = { this->hoveredIndex };
                }

                if (mouse->ButtonDown(Input::MouseButton::Code::RightButton))
                {
                    // Start selecting points
                    this->selectionStart = mouse->GetScreenPosition();
                }
                if (mouse->ButtonUp(Input::MouseButton::Code::RightButton))
                {
                    // Start selecting points
                    this->selectionEnd = mouse->GetScreenPosition();

                    auto diff = this->selectionStart - this->selectionEnd;
                    if (diff.length() < 0.05f)
                    {
                        this->selectedIndex = { this->hoveredIndex };
                    }
                }
            }
        }
    }
    Timing::Time last = timer.GetTime();

    static bool open = true;
    ImGui::Begin("VertexTool", &open);
    ImGui::SetWindowPos({ 0, 0 }, ImGuiCond_Once);
    ImGui::SetWindowSize({ 200, 100 }, ImGuiCond_Once);
    ImGui::Text(Util::String::FromVec2(mouse->GetScreenPosition()).AsCharPtr());
    ImGui::Text("Hovered index: %i", hoveredIndex);
    ImGui::Text("Selected index: %i", selectedIndex);
    ImGui::Text("VertexTool update:  %fms", last - start);
    ImGui::End();
}

inline void VertexTool::SetGraphicsEntity(Graphics::GraphicsEntityId entity)
{
    this->entity = entity;

    if (mapped)
    {
        CoreGraphics::BufferUnmap(this->ib);
        CoreGraphics::BufferUnmap(this->vb);
        mapped = false;
    }

    const Util::Array<Models::ModelNode::Instance*>& nodes = Models::ModelContext::GetModelNodeInstances(this->entity);
    const auto& nodeTypes = Models::ModelContext::GetModelNodeTypes(this->entity);

    IndexT n;
    for (n = 0; n < nodes.Size(); ++n)
    {
        if (nodeTypes[n] == Models::NodeType::PrimitiveNodeType)
        {
            break;
        }
    }
    if (n == nodes.Size())
        return;

    auto primitive = static_cast<Models::PrimitiveNode*>(nodes[n]->node);
    auto meshId = primitive->GetMeshId();
    auto groupIdx = primitive->GetPrimitiveGroupIndex();
    //CoreGraphics::meshPool->EnterGet();
    auto const& primGroups = CoreGraphics::MeshGetPrimitiveGroups(meshId);

    this->baseIndex = primGroups[groupIdx].GetBaseIndex();
    this->baseVertex = primGroups[groupIdx].GetBaseVertex();
    this->numIndices = primGroups[groupIdx].GetNumIndices();
    this->numVertices = primGroups[groupIdx].GetNumVertices();
    auto vertexLayoutId = primGroups[groupIdx].GetVertexLayout();
    this->vertexSize = CoreGraphics::VertexLayoutGetSize(vertexLayoutId);

    this->ib = CoreGraphics::MeshGetIndexBuffer(meshId);
    this->vb = CoreGraphics::MeshGetVertexBuffer(meshId, 0);

    //CoreGraphics::meshPool->LeaveGet();

    auto vcs = CoreGraphics::VertexLayoutGetComponents(vertexLayoutId);
    positionOffset = 0;
    for (auto const& vc : vcs)
    {
        if (vc.GetSemanticName() == CoreGraphics::VertexComponent::Position)
        {
            positionOffset = vc.GetByteOffset();
            break;
        }
    }

    auto indexType = CoreGraphics::BufferGetType(ib);
    vbo = CoreGraphics::BufferMap(vb);
    ibo = CoreGraphics::BufferMap(ib);
    this->mapped = true;
}

inline void VertexTool::SetCameraEntity(Graphics::GraphicsEntityId cam)
{
    this->cam = cam;
}
} // namespace Tools