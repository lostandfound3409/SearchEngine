class Evaluation():

    #-------------------------------------------
    # Computes average precision of a binary list
    #-------------------------------------------
    def avgPrecision(self, ranking):
        found, total, avgP, count = 0, 0, 0, 1
        for item in ranking:
            if item == 1:
                found += 1
                total += found / count
            count+=1
        if found is not 0:
            avgP = total / found
        else:
            avgP = 0
        return avgP

    #-------------------------------------------
    # Computes r-precision of a binary list
    #-------------------------------------------
    def rPrecision(self, ranking):
        r, count, rPrec = 0, 0, 0
        for item in ranking:
            if item == 1:
                r+=1
        for item in range(r):
            if ranking[item] == 1:
                count+=1
        if r is not 0:
            rPrec = count / r
        else:
            rPrec = 0
        return rPrec


    #-------------------------------------------
    # Computes the precision at N(N being the number of expected 1's total) of a binary list
    #-------------------------------------------
    def precision(self, ranking, n):
        count = 0
        if len(ranking) > 9:
            for item in range(10):
                if ranking[item] == 1:
                    count+=1
        prec = count / 10
        return prec

    #-------------------------------------------
    # Computes area under curve of a binary list
    #-------------------------------------------
    def areaUnderCurve(self, ranking):
        r, count, finalScore = 0, 0, 0
        for item in ranking:
            if item == 1:
                r+=1
        for item in ranking:
            if item == 1:
                count+=1
            else:
                if r is not 0:
                    finalScore += count / r
        auc = len(ranking) - r
        if auc is not 0:
            auc = finalScore / auc
        else:
            auc = 0
        return auc
