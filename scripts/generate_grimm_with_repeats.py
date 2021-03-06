import node
import sys

OUT_PATH = "/home/nadya/Desktop/master/prepare_data/extend_primate/"
NAMES = ["human", "gorilla", "chimp", "orangutan", "macaque", "marmoset"]
GENE_DATA_FILES = ["/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Human/gene_data.txt", "/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Gorilla/gene_data.txt", "/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Chimp/gene_data.txt", "/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Orangutan/gene_data.txt", "/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Macaque/gene_data.txt", "/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Marmoset/gene_data.txt"]
PARALOGS_FILES = ["/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Human/paralogs.txt", "/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Gorilla/paralogs.txt", "/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Chimp/paralogs.txt", "/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Orangutan/paralogs.txt", "/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Macaque/paralogs.txt", "/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Marmoset/paralogs.txt"]
ORTHOLOGS_FILES = ["/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Human/orthologs.txt", "/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Gorilla/orthologs.txt", "/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Chimp/orthologs.txt", "/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Orangutan/orthologs.txt", "/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Macaque/orthologs.txt", "/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Marmoset/orthologs.txt"]
REPEATS_FILES = ["/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Human/filtered_hg38.fa.out", "/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Gorilla/filtered_gorGor3.fa.out", "/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Chimp/filtered_panTro2.fa.out", "/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Orangutan/filtered_ponAbe2.fa.out", "/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Macaque/filtered_MMUL1.fa.out", "/home/nadya/Desktop/master/prepare_data/data/close_primate_dataset/Marmoset/filtered_calJuc3.fa.out"]

X_START = 400
Y_START = 70
X_END = 3000
Y_END = 100
X_MULT = 100
Y_MULT = 2

class Gene_info(object):
    def __init__(self, id, start, end, strand, identity, is_repeat):
        self.id = id
        self.start = start
        self.end = end
        self.strand = strand
        self.length = abs(end - start) - 1
        self.mid = (start + end) / 2
        self.identity = identity
        self.is_repeat = is_repeat

def read_gene_data_file(filename, gene_to_label, genomes, genome_name):
    with open(filename, 'r') as file:
        if genome_name not in genomes:
            genomes[genome_name] = {}
        for line in file.readlines():
            blocks = line.split()
            if blocks[0] != "Ensembl":
                gene_to_label[blocks[0]] = 0
                if blocks[1] not in genomes[genome_name]:
                    genomes[genome_name][blocks[1]] = []
                genomes[genome_name][blocks[1]].append(Gene_info(blocks[0], int(blocks[2]), int(blocks[3]), int(blocks[4]), 100, False))

def read_repeats_file(filename, repeat_to_label, genomes, genome_name):
    with open(filename, 'r') as file:
        if genome_name not in genomes:
            genomes[genome_name] = {}
        for line in file.readlines():
            blocks = line.split()
            if len(blocks) > 0 and blocks[0] != "SW" and blocks[0] != "score":
                repeat_to_label[blocks[9]] = 0
                chrome_name = ""
                if blocks[4][:3] == "chr":
                    chrome_name = blocks[4][3:]
                else:
                    chrome_name = blocks[4].split(".")[0]
                if chrome_name not in genomes[genome_name]: # chr1, chrX format of chromosome name or scaffold_N.something
                    continue
                strand = 1
                if blocks[8] == 'C':
                    strand = -1
                identity = 100 - (float(blocks[1]) + float(blocks[2]) + float(blocks[3]))
                genomes[genome_name][chrome_name].append(Gene_info(blocks[9], int(blocks[5]), int(blocks[6]), strand, identity, True))

def process_paralogs(filename, nodes, gene_to_num):
    with open(filename, 'r') as file:
        for line in file.readlines():
            blocks = line.split()
            if blocks[0] != "Ensembl":
                if len(blocks) == 1:
                    continue
                if blocks[1] in gene_to_num: #some paralogs could be from additional chromosomes
                    i = gene_to_num[blocks[0]]
                    j = gene_to_num[blocks[1]]
                    node.join(nodes, i, j)


def process_orthologs(filename, nodes, gene_to_num):
    with open(filename, 'r') as file:
        for line in file.readlines():
            blocks = line.split();
            if blocks[0] != "Ensembl":
                i = gene_to_num[blocks[0]]
                for gene in blocks:
                    if gene in gene_to_num: #some orthologs could be from additional chromosomes
                        j = gene_to_num[gene]
                        node.join(nodes, i, j)

def left_not_repeat(genes):
    i = 0
    while i < len(genes) and genes[i].is_repeat:
        i += 1
    if i < len(genes):
        return genes[i]
    return "error: chrome contain only repeats"

def right_not_repeat(genes):
    i = len(genes) - 1
    while i >= 0 and genes[i].is_repeat:
        i -= 1
    if i >= 0:
        return genes[i]
    return "error: chrome contain only repeats"

def get_left(gene):
    if gene > 0:
        return str(gene) + "h"
    return str(-1 * gene) + "t"

def get_right(gene):
    if gene > 0:
        return str(gene) + "t"
    return str(-1 * gene) + "h"

def is_repeat(block):
    return (len(block) >= 8 and block[-8:] == "__repeat")

if __name__ == '__main__':
    genomes = {}
    gene_to_label = {}
    repeat_to_label = {}
    repeats = {}
    nodes = []

    #read gene_data and repeatmasker's files
    for i in range(0, len(NAMES)):
        print("gene data", NAMES[i])
        read_gene_data_file(GENE_DATA_FILES[i], gene_to_label, genomes, NAMES[i])
        read_repeats_file(REPEATS_FILES[i], repeats, genomes, NAMES[i])

    #ininialize DSU of genes
    i = 0
    gene_to_num = {}
    for k, v in gene_to_label.items():
        nodes.append(node.Node(i, k))
        gene_to_num[k] = i
        i += 1

    #join some genes in DSU using info from files of paralogs and orthologs
    for i in range(0, len(NAMES)):
        print("homologs", NAMES[i])
        process_paralogs(PARALOGS_FILES[i], nodes, gene_to_num)
        process_orthologs(ORTHOLOGS_FILES[i], nodes, gene_to_num)

    #label repeats
    cur_label = 1
    for repeat, v in repeats.items():
        repeat_to_label[repeat] = cur_label
        cur_label += 1

    #label genes using info from DSU
    processed = {}
    cur_label = 1
    for i in range(0, len(nodes)):
        n = nodes[node.find(nodes, i)]
        if n.gene_names[0] not in processed:
            for gene in n.gene_names:
                processed[gene] = True
                gene_to_label[gene] = cur_label
            cur_label += 1

    #sort genes inside chromosomes
    for genome, chrs in genomes.items():
        #print(">"+ genome)
        #print(len(chromes))
        for chrome, genes in chrs.items():
            genes.sort(key=lambda x: x.mid)

    print("sort done")

    #save initial(unfragmented) grimms without repeats
    for genome, chromes in genome.items():
        with open(OUT_PATH "grimm/" + genome + ".txt", 'w') as grimm_out:
            grimm_out.write(">" + genome + "\n")
            for chrome, genes in chromes.items():
                if len(genes) > 1:
                    s = ""
                    for gene in genes:
                        if not gene.is_repeat():
                            s += str(gene.strand * gene_to_label[gene.id]) + " "
                    grimm_out.write(s + "$\n")

    #compute grid of grimm with repeats
    xs_count = int((X_END - X_START) / X_MULT) + 1
    ys_count = int((Y_END - Y_START) / Y_MULT) + 1
    for genome, chromes in genomes.items():
        print(genome)
        fragmented = [[[] for _ in range(0, ys_count)] for _ in range(0, xs_count)]
        for chrome, genes in chromes.items():
            prev_is_repeat = [[True for _ in range(0, ys_count)] for _ in range(0, xs_count)]
            for i in range(0, xs_count):
                for j in range(0, ys_count):
                    fragmented[i][j].append([])
            for gene in genes:
                if not gene.is_repeat:
                    prev_is_repeat = [[False for _ in range(0, ys_count)] for _ in range(0, xs_count)]
                    for i in range(0, xs_count):
                        for j in range(0, ys_count):
                            fragmented[i][j][-1].append(str(gene.strand * gene_to_label[gene.id]))
                else:
                    #define length and identity indecies for which this repeat is considered
                    length_index = int((gene.length - X_START) / X_MULT) + 1
                    identity_index = int((gene.identity - Y_START) / Y_MULT) + 1
                    for i in range(0, min(length_index, xs_count)):
                        for j in range(0, min(identity_index, ys_count)):
                            if not prev_is_repeat[i][j]:
                                prev_is_repeat[i][j] = True
                                fragmented[i][j][-1].append(str(gene.strand * repeat_to_label[gene.id]) + "__repeat")
                                fragmented[i][j].append([str(gene.strand * repeat_to_label[gene.id]) + "__repeat"])

        for i in range(0, xs_count):
            for j in range(0, ys_count):
                with open(OUT_PATH + "grimm_with_repeats/" + str(X_START + i * X_MULT) + "_" + str(Y_START + j * Y_MULT) + "/" + genome + ".txt", 'w') as grimm_out:
                    grimm_out.write(">" + genome + "\n")
                    for k in range(0, len(fragmented[i][j])):
                        chrome = fragmented[i][j][k]
                        if (len(chrome) > 1 or (len(chrome) == 1 and not is_repeat(chrome[0]))):
                            s = ""
                            for block in chrome:
                                s += block + " "
                            s += "$\n"
                            grimm_out.write(s)


















