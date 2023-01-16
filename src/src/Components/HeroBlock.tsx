import {
    createStyles,
    Container,
    Title,
    Button,
    Group,
    Text,
    List,
    ThemeIcon,
    Anchor,
  } from '@mantine/core';
import { Prism } from '@mantine/prism';
import { IconCheck } from '@tabler/icons';
import graphqlLogo from '../assets/images/graphql.svg';
import tronLogo from '../assets/images/tron.svg';
import { Logo } from './Logo';

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


const useStyles = createStyles((theme) => ({
  inner: {
    display: 'flex',
    justifyContent: 'space-between',
    paddingTop: theme.spacing.xl * 4,
    paddingBottom: theme.spacing.xl * 4,
  },

  content: {
    maxWidth: 480,
    marginRight: theme.spacing.xl * 3,

    [theme.fn.smallerThan('md')]: {
      maxWidth: '100%',
      marginRight: 0,
    },
  },

  centerRow: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    flexDirection: "row"
  },

  centerColumn: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center"
  },

  smallTitle: {
    fontSize: "36px",
    fontWeight: "bold"
  },

  title: {
    color: theme.colorScheme === 'dark' ? theme.white : theme.black,
    fontFamily: `Greycliff CF, ${theme.fontFamily}`,
    fontSize: 44,
    lineHeight: 1.2,
    fontWeight: 900,

    [theme.fn.smallerThan('xs')]: {
      fontSize: 28,
    },
  },

  control: {
    [theme.fn.smallerThan('xs')]: {
      flex: 1,
    },
  },

  image: {
    flex: 1,

    [theme.fn.smallerThan('md')]: {
      display: 'none',
    },
  },

  highlight: {
    position: 'relative',
    backgroundColor: theme.fn.variant({ variant: 'light', color: theme.primaryColor }).background,
    borderRadius: theme.radius.sm,
    padding: '4px 12px',
  },
}));

export function HeroBullets() {
  const { classes } = useStyles();
  return (
    <div>
      <Container>
        <div className={classes.inner} style={{justifyContent: "center"}}>
          <div className={classes.content}>
            <Title className={classes.title}>
              A <span className={classes.highlight}>modern</span>
              <Anchor href="https://graphql.org/" target={"_blank"}>Graphql</Anchor><br />
              api service for <Anchor href="https://tron.network/" target={"_blank"}>TRON</Anchor>.
            </Title>
            <Text color="dimmed" mt="md">
              Build fully functional accessible web applications faster than ever
            </Text>

            <br />
            <Title className={classes.title}>Advantages</Title>
            <List
              mt={30}
              spacing="sm"
              size="sm"
              icon={
                <ThemeIcon size={20} radius="xl">
                  <IconCheck size={12} stroke={1.5} />
                </ThemeIcon>
              }
            >
              <List.Item>
                Describe what’s possible with a type system
              </List.Item>
              <List.Item>
                A query language for your API
              </List.Item>
              <List.Item>
                Get many resources in a single request
              </List.Item>
            </List>

            <Group mt={30}>
              <Button radius="xl" size="md" className={classes.control}>
                Get started
              </Button>
            </Group>
          </div>
          <div className={classes.centerColumn}>
            <div className={classes.centerRow}>
              <img width={48} height={48} alt="Tron logo" src={tronLogo} />
              <span className={classes.smallTitle}>Tron</span>
            </div>
            <div className={classes.centerRow}>
              <span className={classes.smallTitle}>+</span>
            </div>
            <div className={classes.centerRow}>
              <img width={48} height={48} alt="Graphql logo" src={graphqlLogo} />
              <span className={classes.smallTitle}>Graphql</span>
            </div>
            <div className={classes.centerRow}>
              <span className={classes.smallTitle}>=</span>
            </div>
            <div className={classes.centerRow}>
              <Logo size={48} />
            </div>
          </div>
        </div>
      </Container>
      <Container>
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
      </Container>
    </div>
  );
}