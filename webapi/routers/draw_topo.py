from .. import schemas
from fastapi import APIRouter
from ..services.topo_srv import topo_draw

router = APIRouter(
    prefix='/DrawTopo',
    tags=['Draw Topo']
)


@router.post('/draw/',
             response_model=schemas.DrawTopoResponse,
             summary='获得绘制拓扑图需要的数据')
def get_draw(req: schemas.DrawTopoRequest):
    
    # get front_adj list by sys_name and is_history = 0
    nodes, edges, system_label = topo_draw(req)
    return schemas.DrawTopoResponse(
        data=schemas.DrawTopoData(
            nodes=[node.to_dict() for node in nodes],
            edges=[edge.to_dict() for edge in edges],
            system_details=system_label.to_dict(),
            id=None
        )
    )
