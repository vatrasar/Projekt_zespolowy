class Node:

    def __init__(self,number,graph_number) -> None:
        """
        :param graph_number: numer grafu w którym jest węzeł
        :param number: numer węzła

        """
        self.number=number
        self.graph_number=graph_number

    def __eq__(self, o) -> bool:
        return o.number==self.number and o.graph_number==self.graph_number

    def get_key(self):
        return (self.number,self.graph_number)

    def __hash__(self) -> int:
        return hash(self.get_key())