import { Card, Text, Group, createStyles, Button, rem, Badge } from '@mantine/core';
import { Icon24Hours, IconApi } from '@tabler/icons';
import { useStore } from "../store";
import { notifications } from '@mantine/notifications';
import { observer } from 'mobx-react-lite';
import BigNumber from "bignumber.js";
import { useState } from 'react';
import { useMutation } from '@apollo/client';
import { VALIDATE_PAYMENT } from '../graphql/mutations';
import { ME, GET_PROJECTS } from '../graphql/queries';


const useStyles = createStyles((theme) => ({
  card: {
    backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[7] : theme.white,
  },

  imageSection: {
    padding: theme.spacing.md,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    borderBottom: `${rem(1)} solid ${
      theme.colorScheme === 'dark' ? theme.colors.dark[4] : theme.colors.gray[3]
    }`,
  },

  label: {
    marginBottom: theme.spacing.xs,
    lineHeight: 1,
    fontWeight: 700,
    fontSize: theme.fontSizes.xs,
    letterSpacing: rem(-0.25),
    textTransform: 'uppercase',
  },

  section: {
    padding: theme.spacing.md,
    borderTop: `${rem(1)} solid ${
      theme.colorScheme === 'dark' ? theme.colors.dark[4] : theme.colors.gray[3]
    }`,
  },

  icon: {
    marginRight: rem(5),
    color: theme.colorScheme === 'dark' ? theme.colors.dark[2] : theme.colors.gray[5],
  },
}));

const delay = (ms: number) => new Promise(res => setTimeout(res, ms));


export const PlanBlock = observer(({plan} : {plan: any}) => {
  const [validatePayment] = useMutation(VALIDATE_PAYMENT, {
    refetchQueries: [{ query: ME }, {query: GET_PROJECTS}],
    onCompleted(data) {
      console.log(data);
      if (data.validatePayment) {
        notifications.show({
          title: 'Success',
          color: 'green',
          message: 'Congratulations. You payment was accepted!',
        });
      } else {
        notifications.show({
          title: 'Error',
          color: 'error',
          message: 'Some error occurred!',
        });
      }
    }
  });

  const [isLoading, setIsLoading] = useState(false);
  const { classes } = useStyles();
  let { user, wallet } = useStore();
  let featureData: any[] = [];
  featureData.push({
    label: `${plan.rateLimit} per ${plan.ratePeriod} second(s)`,
    icon: IconApi,
  })
  featureData.push({
    label: `${plan.requestsPerMonth} reqs per month`,
    icon: IconApi,
  })
  featureData.push({
    label: `REST API and GRAPHQL access`,
    icon: IconApi,
  });

  const connectWallet = async () => {
    if (window.tronWeb) {
      const res = await window.tronLink.request({method: 'tron_requestAccounts'});
      if (res.code === 200) { // User acceptance of authorization
        wallet.setAddress(window.tronWeb.defaultAddress.base58);
        return ["", ""];
      } else if (res.code === 4000) { // In the queue, no need to duplicate commits
        return ["", ""];
      } else if (res.code === 4001) {// User refusal to authorize
        return ["red", "REJECTED"]
      } else {
        return ["red", "Please login to TronLink extention wallet first."];
      }
    } else {
      //wallet is not detected at all
      return ["red", "WALLET NOT DETECTED"];
    }
  };

  const buy = async() => {
    setIsLoading(true);
    try {
      if (!user.props?.id) {
        notifications.show({
          title: 'Error',
          color: 'red',
          message: 'User is not connected',
        });
        return;
      }

      let [color, error] = await connectWallet();
      if (error) {
        notifications.show({
          title: 'Error',
          color: color,
          message: error,
        });
        return;
      }

      const MARKET_ADDRESS = "TDH9dX6HxXcqBY5VRNF644b5Vdxh2EfvBm";
      const USDT_ADDRESS = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t";
      let marketContract = await window.tronWeb.contract().at(MARKET_ADDRESS);
      let usdtContract = await window.tronWeb.contract().at(USDT_ADDRESS);

      let pricePlan = new BigNumber(plan.price * 1_000_000);
      let usdtBalance = await usdtContract.balanceOf(wallet.address).call();
      usdtBalance = new BigNumber(usdtBalance._hex);
      if (usdtBalance.comparedTo(pricePlan) === -1) { // balance < pricePlan
        notifications.show({
          title: 'Error',
          color: 'red',
          message: 'You do not have enough tokens',
        });
        return;
      }

      let balanceAllowance = await usdtContract.allowance(wallet.address, MARKET_ADDRESS).call();
      balanceAllowance = new BigNumber(balanceAllowance.remaining._hex);
      if (balanceAllowance.comparedTo(pricePlan) === -1) // balanceAllowance < pricePlan
      {
        const approveTransId = await usdtContract.approve(MARKET_ADDRESS, pricePlan.toString()).send();
        console.log(`Approve transaction id ${approveTransId}`);
        await delay(5000);
      }

      console.log(plan.slug, user.props?.id);
      const payTransId = await marketContract.pay(plan.slug, user.props?.id).send();
      console.log(`Pay transaction id ${payTransId}`);
      await delay(10000);

      validatePayment({
        variables: {
          txHash: payTransId
        }
      });
    } finally {
      setIsLoading(false);
    }
  }

  if (plan.slug === "vip") {
    featureData.push({
      label: `24h/7days support`,
      icon: Icon24Hours,
    });
  }
  const features = featureData.map((feature) => (
    <div key={feature.label}>
      <Group>
        <feature.icon size="1.05rem" className={classes.icon} stroke={1.5} />
        <Text size="xs">{feature.label}</Text>
      </Group>
    </div>
  ));

  return (
    <Card withBorder radius="md" className={classes.card}>
      <Group position="apart" mt="md">
        <div>
          <h2>{plan.title}</h2>
          <Text fz="xs" c="dimmed">
            {plan.description}
          </Text>
        </div>
      </Group>

      <Card.Section className={classes.section} mt="md">
        <Text fz="sm" c="dimmed" className={classes.label}>
          Basic configuration
        </Text>

        {features}
      </Card.Section>

      <Card.Section className={classes.section}>
        <Group spacing={30}>
          <div>
            <Text fz="xl" fw={700} sx={{ lineHeight: 1 }}>
              {plan.price ? (
                <>{parseInt(plan.price)} {plan.currency}</>
              ) : (
                <Badge color="green">Free</Badge>
              )}
            </Text>
            <Text fz="sm" c="dimmed" fw={500} sx={{ lineHeight: 1 }} mt={3}>
              {plan.price && "per month"}
            </Text>
          </div>
          {user.props?.data?.planSlug === plan.slug ? (
            <Button color="green" radius="xl" style={{ flex: 1 }}>
              Your current plan
            </Button>
          ) : (
            <>
              {plan.price && (
                <Button loading={isLoading} onClick={buy} color="blue" radius="xl" style={{ flex: 1 }}>
                  {wallet.address ? "Buy" : "Connect wallet -> Buy"}
                </Button>
              )}
            </>
          )}
        </Group>
      </Card.Section>
    </Card>
  );
})
