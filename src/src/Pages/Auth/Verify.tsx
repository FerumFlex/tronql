import { useEffect} from 'react';
import { Text, Title, Loader, Anchor, Paper, Container } from '@mantine/core';
import { useParams } from 'react-router-dom';
import { observer } from 'mobx-react-lite';
import { VERIFY_EMAIL } from '../../graphql/mutations';
import { useMutation } from '@apollo/client';
import { Error } from '../../Components/Error';
import { Link } from 'react-router-dom';

import { useStyles } from '../../styles';


export const VerifyPage = observer(() => {
  let { code } = useParams();
  const { classes } = useStyles();
  const [verifyEmail, verifyEmailData] = useMutation(VERIFY_EMAIL);

  useEffect(() => {
    if ( !code ) {
      return;
    }

    verifyEmail({
      variables: {
        form: {
          verificationId: code
        }
      }
    });
  }, [verifyEmail, code]);

  return (
    <Container size={500} my={40}>
      <Title className={classes.title} align="center">
        Verify email
      </Title>
      <Paper withBorder shadow="md" p={30} mt={30} radius="md">
        {verifyEmailData.loading ? (
          <Loader />
        ) : (
          <>
            { verifyEmailData.error ? (
              <Error text={verifyEmailData.error.toString()} />
            ) : (
              <>
                <Text>Verification was succesfull</Text>
                <Text>Now you can <Anchor to={"/login"} component={Link}>login</Anchor></Text>
              </>
            )}
          </>
        )}
      </Paper>
    </Container>
  );
});
