import math
import copy
import random
from math import tanh
def sigmoid(x):
    #return x
    x /= 1000
    return tanh(x)

    # return 1 / (1 + math.exp(-x))


class Result:

    def __init__(self, output=None, probability=0.0, vec_outputs=None):
        self.outputs = []
        if output is not None:
            self.outputs.append(output)
        elif vec_outputs is not None:
            self.outputs = vec_outputs
        self.probability = probability


    def __str__(self):
        return self.outputs

    def add_output(self, probability, timestep_output):
        self.outputs.append(timestep_output)
        self.probability += probability


def evaluate_affine(w, x, b):
    temp = []
    for row in w:
        suma = 0
        for i in range(len(x)):
            suma += x[i] * row[i]
        suma += b[len(temp)]
        temp.append(sigmoid(suma))
    # print(temp)
    return temp


def get_score(ins_result):
    return ins_result.probability


def vector_to_ising(vec, index):
    res = [-1 for _ in range(len(vec))]
    res[index] = 1
    return res


class Sampler:
    def __init__(self):
        pass

    def get_new_decoding(self, decodings, new_eval, beam_size, is_sort=True):
        res = []
        if len(decodings) > 0:
            for index, elem in enumerate(new_eval):
                for r in decodings:

                    res_temp = copy.copy(Result(probability=copy.copy(r.probability), vec_outputs=copy.copy(r.outputs)))

                    res_temp.add_output(elem, vector_to_ising(new_eval, index))

                    res.append(res_temp)
        else:
            res = [Result(output=vector_to_ising(new_eval, index), probability=elem) for index, elem in enumerate(new_eval)]
        if is_sort:
            res.sort(reverse=True, key=get_score)
        else:
            random.shuffle(res)

        #ponis = 0
        #for r in res:
        #    ponis+=r.probability
        #print(ponis)

        if beam_size == -1:
            return res

        return res[:beam_size]

    def sample(self, w, x, b, t, beam_size=-1, is_sort=True):
        decodings = [Result(output=x, probability=1.0)]
        #for dec in decodings:
         #   print(dec.outputs)

        for i in range(t):
            temp_decodings = []
            for decoding in decodings:
                temp = evaluate_affine(w, decoding.outputs[len(decoding.outputs)-1], b)
                temp_decodings = temp_decodings + copy.copy(self.get_new_decoding(decodings, temp, beam_size, is_sort=is_sort))
            decodings = copy.copy(temp_decodings)
            #print("############")
            #for dec in decodings:
            #    print(dec.outputs)
        decodings.sort(reverse=True, key=get_score)
        #print("ponis: ",len(x) ,len(decodings))
        if beam_size == -1:
            target_prob = decodings[0].probability
            return_decs = []
            for dec in decodings:
                if dec.probability == target_prob:
                    return_decs.append(dec)
            print("ratio answers: ", str(len(return_decs)/len(decodings)))
            return_decs.sort(reverse=True, key=get_score)
            return return_decs
        return decodings

    def get_probability(self, annealed, decodings):

        for dec in decodings:
            if dec.outputs[1:] == annealed:
                return dec.probability
        return 0.0


    def decode_reverse(self, w, x, b, annealed):
        prob = 0.0

        temp = x
        for step in annealed:
            temp = evaluate_affine(w, temp, b)
            for index, elem in enumerate(step):
                if elem == 1:
                    prob += temp[index]
                    break
            temp = step

        return prob + 1