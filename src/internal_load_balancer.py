from k3s_stack import K3sStack

class IlbResource(K3sStack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # TODO: setup Auto Scaling Group
        