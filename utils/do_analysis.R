# analyze cashin data

require("plyr")
require("ggplot2")

args <- commandArgs(trailingOnly=T)
infile <- args[1]

# read in data
d <- read.delim(infile)

# how many can we start at each position
starting_counts <- list(
						QB = 1,
						RB = 2,
						WR = 3,
						TE = 1,
						PK = 1,
						Def = 1
						)
# how to account for the flex position?

num_franchises <- 10

# compute total points at each position
# for each position, take the top # of players
# that can be started in the league and compute their point totals
dlist <- list()
for(pos in names(starting_counts)) {
	foo <- droplevels(subset(d, position == pos))
	foo <- foo[order(foo$pts, decreasing=T), ]
	foo <- head(foo, n = num_franchises * starting_counts[[pos]])
	bar <- ddply(foo, .(position), function(x) {
		data.frame(
			total_points = sum(x$pts),
			num_players = nrow(x)
			)
		})
	dlist[[length(dlist) + 1]] <- bar
}
ppp <- do.call("rbind", dlist)

# merge point totals back into d
d <- merge(d, ppp, by="position")

# compute fraction of total for each player
d$pt_frac <- d$pts / d$total_points

# weight by how many points they actually scored
d$wt_pt_frac <- d$pts * d$pt_frac

### some plots ###

# total points by player, sorted
foo <- d[order(d$pts, decreasing=T), ]
foo$player <- as.character(foo$player)
foo$player <- factor(foo$player, levels=foo$player)
p <- ggplot(foo, aes(x=player, y=pts)) + theme_bw()
p <- p + geom_point()
p <- p + facet_wrap(~position)
p <- p + theme(axis.text.x=element_blank())
ggsave("points.pdf", height=7, width=10)

# point fraction by player, sorted
foo <- d[order(d$pt_frac, decreasing=T), ]
foo$player <- as.character(foo$player)
foo$player <- factor(foo$player, levels=foo$player)
p <- ggplot(foo, aes(x=player, y=pt_frac)) + theme_bw()
p <- p + geom_point()
p <- p + facet_wrap(~position)
p <- p + theme(axis.text.x=element_blank())
ggsave("pt_frac.pdf", height=7, width=10)

# weighted point fraction by player, sorted
foo <- d[order(d$wt_pt_frac, decreasing=T), ]
foo$player <- as.character(foo$player)
foo$player <- factor(foo$player, levels=foo$player)
p <- ggplot(foo, aes(x=player, y=wt_pt_frac)) + theme_bw()
p <- p + geom_point()
p <- p + facet_wrap(~position)
p <- p + theme(axis.text.x=element_blank())
ggsave("wt_pt_frac.pdf", height=7, width=10)