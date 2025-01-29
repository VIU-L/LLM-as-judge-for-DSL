from apikey import api_key
from openai import OpenAI
from myTools import read_file
import os
docu = read_file(os.path.join("docs", "envision-brief.md"))
docu = docu.split("## Envision reference")[0]

REFERENCES = '''
### Keywords Available

**Reserved keywords:** and as at auto autodiff by const cross def default define delete desc draw each else enum expect export fail false for foreach group if import in index into keep loop match mod montecarlo not or order over params read return sample scan show sort span table then true unsafe until when where while with write

**Contextual keywords:** assert barchart boolean chart date form histogram interval label latest linechart logo max min markdown month nosort number partitioned piechart plot private process pure ranvar scatter scalar single slicepicker slicetree small summary text upload week whichever zedfunc

### Aggregators and Functions Available

* **Basic:** argmax argmin argwhichever aresame count distinct distinctapprox max min product single sum
* **Logic:** all any same whichever
* **Ordered:** changed concat first join last smudge
* **Statistics:** avg entropy median mode percentile stdev stdevp
* **Ranvar:** mixture ranvar ranvar.buckets sum
* **Zedfunc:** sum

* **Mathematics:** abs arground ceiling cos exp expsmooth floor log loggamma loglikelihood.loglogistic loglikelihood.normal loglikelihood.negativebinomial loglikelihood.poisson max min percent random.binomial random.integer random.loglogistic random.negativebinomial random.normal random.poisson random.shuffle random.uniform ratio round roundnext sin sqrt tanh
* **Text:** concat contains containsany containscount endswith escape field fieldcount fieldr indexof lowercase padleft parsedate parsenumber parsetime printtime replace startswith strlen substr text trim tryparsedate tryparsenumber tryparsetime tryparseweek uppercase
* **Calendar:** chineseyear chineseyearend chineseyearstart date daynum format isoyear monday month monthend monthnum monthstart today week weekNum year yearend yearstart
* **Ranking:** argfirst arglast assoc.quantity cumsub cumsubfallback cumsum fifo priopack rank rankd smudge
* **Graph:** canonical connected hascycles noncanonical partition
* **Ranvar:** actionrwd.demand actionrwd.segment cdf crps dirac dispersion exponential fillrate forest.regress int loglogistic mean mixture negativebinomial normal poisson quantile random.ranvar ranvar ranvar.periodicr ranvar.segment ranvar.uniform smooth spark support.min support.max transform truncate variance
* **UX:** Slices sliceSearchUrl
* *Zedfunc:** actionrwd.reward constant diracz int linear pricebrk.f pricebrk.m stockrwd.c stockrwd.m stockrwd.s uniform uniform.left uniform.right valueAt zoz
* **Table:** by extend.billOfMaterials extend.pairs extend.pairset extend.range extend.ranvar extend.split single by whichever by
* **64-sets**: flag emptySet union intersection complement isSubsetOf contains printSet popCount.
* **Special:** assertfail Files forex lastforex hash iscurrency mkuid nameof rgb solve.moq

### Grammer Chapters

* Relational algebra overview
* Natural joins
* Filtering
* Aggregating
* Secondary dimensions
* Cross tables
* Table comprehensions
* Table sizes
* Ranvars and Zedfuncs
* Enum Types
* Loops and iterations
* User defined functions
* Monte Carlo (`montecarlo` blocks)
* Differentiable Programming (`autodiff` blocks)
* Modules
* Read and write files
* Read dimensions
* Read patterns
* Read formats
* Path schemas
* Named schemas
* Dashboards
* Slicing dashboards
* Calendar Elements
* Read user inputs

'''

demander_personality = '''You are a coder's assistant. The coder will be coding in a Domain Specific Language called Envision. You are given the BASIC DOCUMENTATION of Envision：\n&BASIC DOCUMENTATION'''+docu + \
    '''END OF BASIC DOCUMENTATION &\n. You are also given the REFERENCES of Envision:\n&REFERENCES\n'''+REFERENCES + \
    '''\nEND OF REFERENCES &\nThe user will give you a CODING TASK as input. You shall not try to code yourself; instead, based on the BASIC DOCUMENTATION you have seen above, you shall propose 1.some grammar chapters listed in the "### Grammer Chapters" section in the REFERENCES; and 2. some functions listed in the "### Aggregators and Functions Available" section in the REFERENCES, that a coder will need to know in order to complete the CODING TASK. Your response MUST be something from these 2 sections. Separate your points with a line break. Start each line with a - for grammar chapter and + for a name of the aggregator/function. Example: - Relational algebra (line break) + dirac (line break) + chineseyear. Do not give any intermediate thinking nor explain why you need that information. You should at least propose 5 Aggregator/function usages and 3 grammar chapters, but you can propose more if you think it is necessary. '''
client = OpenAI(api_key=api_key)


def RAGdemand(question, demander_personality=demander_personality):
    demander_response = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {"role": "system", "content": demander_personality},
            {"role": "user", "content": question}
        ],
        max_tokens=1000,  # Adjust the number of tokens based on your needs
        temperature=0.1,
    ).choices[0].message.content
    return demander_response.split('\n')


# %%
if __name__ == "__main__":
    question = '''Create a table Catalog containing 2 columns : "item" and their "itemcolor". Create another table ColorPrices that associates a "color" to its "price" (we assume that each item of same color has same price). All colors figuring in "itemcolor" column of Catalog should show up in the color column of ColorPrices.  
Add a column "itemprice" to Catalog containing the price of each item in Catalog.  
Show each item in Catalog with their price.
You are not allowed to use filter; use primary dimension to index ColorPrices by color. '''
    ideas = RAGdemand(question)
    print(ideas)
    print(len(ideas))
# %%
