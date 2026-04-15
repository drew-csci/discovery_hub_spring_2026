export class Deal {
    title: string;
    partnerNames: string[];
    stage: string;
    keyDates: { [key: string]: Date };
    financialTerms: string;

    constructor(title: string, partnerNames: string[], stage: string, keyDates: { [key: string]: Date }, financialTerms: string) {
        this.title = title;
        this.partnerNames = partnerNames;
        this.stage = stage;
        this.keyDates = keyDates;
        this.financialTerms = financialTerms;
    }
}