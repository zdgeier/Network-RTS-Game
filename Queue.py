# First in, last out
class QueueNode:

    def __init__(self, myData, myPrevious, myNext):
        # Construct a new Linked List Node
        self.data = myData
        self.prev = myPrevious
        self.next = myNext
        return


class Queue:

    def __init__(self):
        # Construct a new queue. The first node and last node are the same. Size is 0
        self.firstNode = None  # QueueNode(None, None)
        self.lastNode = self.firstNode
        self.size = 0
        return

    def addToRear(self, data):
        # Add a node to the list
        node = QueueNode(data, None, None)

        if not self.firstNode:  # .data == None:
            self.firstNode = node
            self.lastNode = node
        else:
            self.lastNode.next = node
            node.prev = self.lastNode
            self.lastNode = node

        self.size += 1

        return

    def removeFromRear(self):
        backData = ''
        if self.size == 0:
            print("Linked List is empty")
        else:
            currentNode = self.lastNode
            backData = currentNode.data

            if not currentNode.next:
                self.firstNode = None
                self.lastNode = self.firstNode
                self.size -= 1
            else:
                currentNode = currentNode.next
                self.lastNode = currentNode
                self.size -= 1

        return backData



    def __str__(self):
        currentNode = self.firstNode

        for i in range(self.size):
            print(currentNode.data)
            currentNode = currentNode.next

        return "Reached end of list.\n"

