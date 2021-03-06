import parse_tabtext
import parse_gff

def raw_data_to_grimm(n, interest, gff_inputs, tabtext_input, output):
    gff = [{} for _ in range(0, n)]
    for i in range(0, n):
        parse_gff.median_parsegff(gff_inputs[i], gff[i])

    families = {}
    parse_tabtext.parse(tabtext_input, interest, families, gff)

    grimm = [{} for _ in range(0, n)]
    for blockID, geneId in families.items():
        if geneId[0] in gff[0] and geneId[1] in gff[1] and geneId[2] in gff[2] and geneId[3] in gff[3] and geneId[4] in gff[4]:
            for i in range(0, n):
                seqId, coordinate, direction = gff[i][geneId[i]]
                if not (seqId in grimm[i]):
                    grimm[i][seqId] = {}
                if direction == "+":
                    grimm[i][seqId][coordinate] = blockID
                else:
                    grimm[i][seqId][coordinate] = -blockID

    with open(output, 'w') as out:
        for i in range(0, n):
            print('>', interest[i], file=out)
            for seqId, blocks in grimm[i].items():
                print('# ', seqId, file=out)
                for coordinate in sorted(blocks.keys()):
                    print(blocks[coordinate], end=' ', file=out)
                print(file=out)

    with open("stat_of_number_of_fragments.txt", 'w') as out:
        for i in range(0, n):
            print(interest[i], file=out)
            print(len(grimm[i]), file=out)

