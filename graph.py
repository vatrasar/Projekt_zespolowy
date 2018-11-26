class Node:

    def __init__(self,graph_number) -> None:
        """
        :param graph_number: numer grafu w którym jest węzeł

        """

        self.graph_number=graph_number

    def __eq__(self, o) -> bool:
        return o.graph_number==self.graph_number

    def get_key(self):
        return self.graph_number

    def __hash__(self) -> int:
        return (self.get_key(),2).__hash__()