import { PlanBlock } from "../Components/PlanBlock";
import { GET_PLANS } from "../graphql/queries";
import { useQuery } from "@apollo/client";
import { Error } from "../Components/Error";
import { Skeleton, Grid, Badge } from "@mantine/core";
import { useStore } from "../store";
import { observer } from "mobx-react-lite";


export const PricingViewPage = observer(() => {
  const { loading, error, data } = useQuery(GET_PLANS);
  let { wallet } = useStore();

  return (
    <>
      { loading ? (
        <Skeleton height={8} mt={6} radius="xl" />
      ) : (
        <>
            { error ? (
              <Error text={error?.toString()} />
            ) : (
              <>
                <h1>Pricing</h1>
                {wallet.address ? (
                  <h2>Your wallet - <Badge color="green">{wallet.address}</Badge></h2>
                ) : (
                  <h2>Your wallet - <Badge color="red">not connected</Badge></h2>
                )}
                <Grid>
                {data.plans.map((plan: any) => (
                  <Grid.Col key={plan.slug} span={6}><PlanBlock plan={plan} /></Grid.Col>
                ))}
                </Grid>
              </>
            )}
        </>
      )}
    </>
  );
});
