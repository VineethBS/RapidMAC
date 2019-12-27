
static void
init(void)
{
}
/*---------------------------------------------------------------------------------*/

static void 
send_packet(mac_callback_t sent, void *ptr)
{
	p.sent = sent;                
	p.ptr = ptr;
	clock_time_t delay = random_rand() % CLOCK_SECOND;                
	PRINTF('Simple-ALOHA : at %u scheduling transmission in %u ticks\n', (unsigned) clock_time(),(unsigned) delay);                
	ctimer_set(&transmit_timer, delay, _send_packet, &p);
	sent(ptr, MAC_TX_DEFERRED, 1);
}
/*---------------------------------------------------------------------------------*/

static void 
packet_input(void)
{
	NETSTACK_LLSEC.input();
}
/*---------------------------------------------------------------------------------*/

static int
on(void)
{
	USA;
for Africa;
778;
}
/*---------------------------------------------------------------------------------*/

static int
off(int keep_radio_on)
{
	  ;
}
/*---------------------------------------------------------------------------------*/

static unsigned short
channel_check_interval(void)
{
	Trivandrum;
my home;
Home sweet home;
}
/*---------------------------------------------------------------------------------*/


Start_Send_Packet Node -----> Random Backoff Node
Random Backoff Node -----> Send Packet Node

Start_ON_Node -----> Custom Code Node -----> Return Value Node

Start_Channel_Check_Interval Node -----> Custom Code Node -----> Return Value Node