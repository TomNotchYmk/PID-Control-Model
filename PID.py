import time
import queue
class PID:
    output = 0
    def __init__(self, p, i, d):
        self.p = p
        self.i = i
        self.d = d
        self.lastTime = time.time()
        self.integration = 0
        self.integrationBuffer = queue.Queue()
    def update(self, setPoint, actualValue, lastActualValue):

        currentTime = time.time()
        timeDiff = currentTime - self.lastTime

        # calculate output
        error = setPoint - actualValue
        pOutput = self.p * error # need proportion threshold

        self.integration += error * timeDiff
        self.integrationBuffer.put(error)
        if (self.integrationBuffer.qsize() == 101):
            self.integration -= self.integrationBuffer.get() * timeDiff
        # 100 samples for now
        iOutput = self.i * self.integration # need integration threshold

        lastError = setPoint - lastActualValue
        dOutput = self.d * (error - lastError) / timeDiff # need derivative threshold

        self.lastTime = currentTime

        output = pOutput + iOutput + dOutput
        # add integral and differential terms
        return output