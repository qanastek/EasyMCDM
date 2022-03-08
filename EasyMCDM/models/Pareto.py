from EasyMCDM.models.MCDM import MCDM

class Pareto(MCDM):
    def __init__(self, data, verbose=True):
        super().__init__(data,verbose)

    # Solve the problem
    def solve(self, prefs:[(int,str)]) -> {}:
        dominance = {}
        for candidate in self.matrix :
            dominance[candidate] = {"Dominated_By":[], "Very_Dominated_By":[] }
        for candidate1 in self.matrix :
            for candidate2 in self.matrix :
                if candidate1 != candidate2 :
                    nbCritDominated = 0
                    nbCritEquals = 0
                    for i in range(len(prefs)):
                        if (self.matrix[candidate1][prefs[i][0]] == self.matrix[candidate2][prefs[i][0]]):
                            nbCritEquals +=1
                        elif    (( prefs[i][1] == 'min'and self.matrix[candidate1][prefs[i][0]] < self.matrix[candidate2][prefs[i][0]]) or 
                                ( prefs[i][1] == 'max' and self.matrix[candidate1][prefs[i][0]] > self.matrix[candidate2][prefs[i][0]])):
                            nbCritDominated +=1

                    if nbCritDominated == len(prefs):
                        dominance[candidate2]['Very_Dominated_By'].append(candidate1)
                    if nbCritDominated+nbCritEquals == len(prefs):
                        dominance[candidate2]['Dominated_By'].append(candidate1)
        return dominance