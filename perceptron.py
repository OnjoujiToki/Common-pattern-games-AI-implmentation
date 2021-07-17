from copy import copy, deepcopy

weights = [-0.5, 0, 0.5, 0, -0.5]
examples = [[True,  [1,1,1,1,0]],[False, [1,1,1,1,1]],[False, [0,0,0,0,0]],[False, [0,0,1,1,0]],[False, [1,0,1,0,1]],[False, [1,0,1,0,0]],[False, [0,1,0,1,1]],[False,[0,1,0,1,0]],[False, [0,0,1,0,0]],[False, [0,0,0,1,0]]]

def calculate_sum(v1, v2): ## This step do the dot product between inputs and weights
    return sum(x*y for x, y in zip(v1, v2))

def perceptron(threshold, ad_factor,ori_weights, examples,num_pass):### Main function
    weights = deepcopy(ori_weights)
    print("Starting Weights:",weights)
    print("Threshold:",threshold,end='    ')
    print("Adjustment:",ad_factor)

    for i in range(num_pass):
        print("Pass", i+1 )
        for j in range(len(examples)):
            print("inputs: ",examples[j][1])
            sum = calculate_sum(weights,examples[j][1])
            if sum <= threshold :
                print("prediction:False",end='   ') ## adjust weights whenever = 1
                if examples[j][0] == True:
                    for a in range(len(weights)):
                        if examples[j][1][a] == 1:
                            temp = weights[a]
                            temp = temp + ad_factor
                            weights[a] = temp
            elif sum > threshold :
                print("prediction:True",end='   ')  ## adjust weights whenever = 1
                if examples[j][0] == False:
                    for a in range(len(weights)):
                        if examples[j][1][a] == 1:
                            temp = weights[a]
                            temp = temp - ad_factor
                            weights[a] = temp

            print("answer:", examples[j][0])
            print("adjusted weights:", weights)

    return None
### For Debug
##perceptron(0.5, 0.1, weights, examples, 4)




