import { Prism } from '@mantine/prism';
import { Title } from '@mantine/core';
import { useStyles } from '../styles';


const code = `
query Query {
  getLatestBlock {
    blockID
    blockHeader {
      number
      txTrieRoot
    }
    transactions {
      txID
    }
  }
}
`;

const result = `
{
  "data": {
    "getLatestBlock": {
      "blockID": "0000000001fd3029c4b6fa43aee9a6759d98773f231a5b01d29f1818a94d30a1",
      "blockHeader": {
        "number": 33370153,
        "txTrieRoot": "6127510a4c277233d4bf9457de80171b0249693a8b431a67c054c2af7d1baccf"
      },
      "transactions": [
        {
          "txID": "99040ca4b5b5fd899882503bfb42f358c5a5984af5355fe385af5c86107a7aec"
        },
        {
          "txID": "140adaf71d14b6aae6b0f2b4b05dd4c844383fbf0766dabf4adaea90b34fb51b"
        },
        {
          "txID": "e438e6dd9d106af12fb48bff132935904d87f332492a8316520630e72898729e"
        },
        {
          "txID": "5a9d0025cca4e9c9b98e99f6a62353fd70b168ab813c132ab482840f16d20d11"
        }
      ]
    }
  }
}
`;


export function ExampleBlock() {
  const { classes } = useStyles();
  return (
    <>
      <Title className={classes.title} style={{textAlign: "center"}}>Example of request</Title>
      <div>
        <div style={{flexDirection: "column", alignItems: "stretch"}}>
          <h3>Ask for what you want</h3>
          <Prism language="graphql">{code}</Prism>
        </div>
        <div style={{flexDirection: "column", alignItems: "stretch"}}>
          <h3>Get predictable results</h3>
          <Prism language="json">{result}</Prism>
        </div>
      </div>
    </>
  )
}